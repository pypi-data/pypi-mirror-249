from alibabacloud_tea_openapi.models import Config as SessionConfig

from .tea_api import AliCloudTeaApi, auto_pagination


class ResourceCenterManager(AliCloudTeaApi):
    def __init__(self, config: SessionConfig):
        super().__init__(config, "2022-12-01", endpoint="resourcecenter.aliyuncs.com")

    @property
    def service_status(self):
        status = self.call_api("GetResourceCenterServiceStatus")
        return status

    def enable(self):
        return self.call_api("EnableResourceCenter")

    def disable(self):
        return self.call_api("DisableResourceCenter")

    @auto_pagination(["Resources"])
    def search_resource_cross_account(self, q_str, next_token=None, page_size=100):
        queries = {
            "Scope": q_str,
            "MaxResults": page_size
        }
        if next_token:
            queries["NextToken"] = next_token
        return self.call_api("SearchMultiAccountResources", queries)

    @auto_pagination(["Resources"])
    def search_resource_this_account(self, next_token=None, page_size=100):
        queries = {
            "MaxResults": page_size
        }
        if next_token:
            queries["NextToken"] = next_token
        return self.call_api("SearchResources", queries)

    def describe_resource_cross_account(self, account_id, resource_region, resource_type, resource_id):
        queries = {
            'AccountId': account_id,
            'ResourceRegionId': resource_region,
            'ResourceType': resource_type,
            'ResourceId': resource_id
        }
        return self.call_api("GetMultiAccountResourceConfiguration", queries)

    def describe_resource_this_account(self, resource_region, resource_type, resource_id):
        queries = {
            'ResourceRegionId': resource_region,
            'ResourceType': resource_type,
            'ResourceId': resource_id
        }
        return self.call_api("GetResourceConfiguration", queries)
