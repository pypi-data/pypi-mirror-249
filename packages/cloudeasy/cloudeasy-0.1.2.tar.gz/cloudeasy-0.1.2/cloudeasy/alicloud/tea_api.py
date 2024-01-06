import logging
from typing import TypeVar, ParamSpec, List, Callable

import Tea.exceptions
from Tea.exceptions import UnretryableException
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi.models import Config as SessionConfig
from alibabacloud_tea_util import models as util_models
from requests.exceptions import ConnectionError


class ServiceNotEnabled(Exception):
    pass


class PleaseRetryError(Exception):
    pass


class ServerInternalError(Exception):
    pass


P = ParamSpec("P")
R = TypeVar("R")


def auto_pagination(nodes: List[str] = None) -> Callable[P, R]:
    if nodes is None:
        nodes = []

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            while True:
                response = func(*args, **kwargs)
                content: dict = response
                if response is not None:
                    for _node in nodes:
                        content = content.get(_node, {})
                yield content
                match response:
                    case {"NextToken": token}:
                        # api pagination is via next token
                        kwargs["next_token"] = token
                    case {"PageSize": page_size, "TotalSize": total_size, "CurrentPage": page_no} | \
                         {"PageSize": page_size, "TotalCount": total_size, "PageNumber": page_no}:
                        # api pagination is via page no and total account
                        if page_no < total_size // page_size + 1:
                            kwargs["page_no"] = page_no + 1
                            kwargs["page_size"] = page_size
                        else:
                            break

                    case _:
                        break

        return wrapper

    return decorator


P2 = ParamSpec("P2")
R2 = TypeVar("R2")


def tea_request_wrapper(func: Callable[P2, R2]) -> Callable[P2, R2]:
    def wrapper(*args: P2.args, **kwargs: P2.kwargs) -> R2:
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            exception = PleaseRetryError("Network ssl error,please retry")
        except UnretryableException as e:
            exception = PleaseRetryError(e.inner_exception.message)
        except Tea.exceptions.TeaException as e:
            error_data = e.args[0]['data']
            error_code = error_data['Code']
            error_code_type = error_code.split('.')[0]

            match error_code_type:
                case 'Throttling' | 'InternalError':
                    exception = PleaseRetryError(error_data)
                case 'NoPermission':
                    if error_data.get("AccessDeniedDetail"):
                        recommend = f"https://ram.console.aliyun.com/permissions/troubleshoot with code {error_data['AccessDeniedDetail']}"
                    else:
                        recommend = error_data['Recommend']
                    exception = PermissionError(f"""{error_data['Message']}
                        recommend: {recommend}
                        """)
                case 'UnauthorizedOperation' | 'CdnServiceNotFound' | 'DcdnServiceNotFound':
                    """maybe service didn't enabled"""
                    exception = ServiceNotEnabled(f"Ignored {error_data}")
                case _:
                    exception = ServerInternalError(f"""{error_data['Message']}
                    recommend: https://api.aliyun.com/troubleshoot?q={error_data['RequestId']}
                    """)
        if exception is not None:
            raise exception

    return wrapper


class AliCloudTeaApi:
    request_wrapper = tea_request_wrapper

    def __init__(self, config: SessionConfig, version, endpoint=None):
        self.config = config
        if endpoint:
            self.config.endpoint = endpoint
        self.client = OpenApiClient(self.config)
        self.options = util_models.RuntimeOptions()
        self.version = version

    @request_wrapper
    def call_api(self, action, queries=None, **kwargs):
        kwargs_params = {
            "body_type": "json",
            "req_body_type": "json",
            "protocol": "HTTPS",
            "auth_type": self.client.get_type(),
            "method": "POST",
            "style": "RPC",
            "pathname": "/",
            "version": self.version,
            "action": action
        }
        kwargs_params.update(kwargs)
        params = open_api_models.Params(**kwargs_params)
        request = open_api_models.OpenApiRequest()
        if queries:
            request.query = OpenApiUtilClient.query(queries)
        try:
            response = self.client.call_api(params, request, self.options)
            assert response['statusCode'] // 100 == 2
            return response['body']
        except KeyError:
            logging.error(f'Failed to call api {kwargs}')
        except AssertionError:
            logging.error("Failed")
