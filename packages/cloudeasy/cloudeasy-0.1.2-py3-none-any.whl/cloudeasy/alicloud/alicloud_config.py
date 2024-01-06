from alibabacloud_tea_openapi.models import Config as SessionConfig


class AliCloudConfig(object):

    @classmethod
    def from_ak_sk(cls, ak: str, sk: str, **kwargs) -> SessionConfig:
        return SessionConfig(
            access_key_id=ak,
            access_key_secret=sk,
            **kwargs
        )
