from alibabacloud_tea_openapi.models import Config as SessionConfig

from .tea_api import AliCloudTeaApi, auto_pagination


class DnsManager(AliCloudTeaApi):
    def __init__(self, config: SessionConfig):
        super().__init__(config, "2015-01-09", endpoint="alidns.cn-shanghai.aliyuncs.com")

    @auto_pagination(["Domains", "Domain"])
    def list_domains(self, page_no=1, page_size=50):
        return self.call_api(
            "DescribeDomains",
            {
                "PageSize": page_size,
                "PageNumber": page_no
            }
        )

    @auto_pagination(["DomainRecords", "Record"])
    def list_dns_resource_records(self, domain: str, page_no=1, page_size=50, **kwargs):
        # see https://next.api.aliyun.com/document/Alidns/2015-01-09/overview for full kwargs
        query = {
            "PageSize": page_size,
            "PageNumber": page_no,
            "DomainName": domain
        }
        if kwargs:
            query.update(kwargs)
        return self.call_api(
            "DescribeDomainRecords",
            query
        )

    def query_resource_record(self, domain: str, hostname: str):
        return self.list_dns_resource_records(domain, KeyWord=hostname, SearchMode="EXACT")

    def add_resource_record(self, hostname: str, domain: str, resource_type: str, resource_data: str, ttl=None, priority=None, line=None, language=None):
        # line: https://help.aliyun.com/document_detail/29807.html
        query = {
            "DomainName": domain,
            "RR": hostname,
            "Type": resource_type.upper(),
            "Value": resource_data,
        }
        if ttl:
            query["TTL"] = ttl
        if priority:
            query["Priority"] = priority
        if line:
            query["Line"] = line
        if language:
            query["Lang"] = language
        return self.call_api(
            "AddDomainRecord",
            queries=query
        )

    def get_resource_record(self, aliyun_resource_id: str, language=None, client_ip=None):
        query = {
            "RecordId": aliyun_resource_id
        }
        if language:
            query["Lang"] = language
        if client_ip is not None:
            query["UserClientIp"] = client_ip
        return self.call_api(
            "DescribeDomainRecordInfo",
            queries=query
        )

    def update_resource_record(self, aliyun_record_id: str, hostname: str, resource_type: str, resource_data: str, ttl=None, priority=None, line=None, language=None):
        query = {
            "RecordId": aliyun_record_id
        }
        if hostname:
            query["RR"] = hostname
        if resource_data:
            query["Value"] = resource_data
        if resource_type:
            query["Type"] = resource_type
        if ttl:
            query["TTL"] = ttl
        if priority:
            query["Priority"] = priority
        if line:
            query["Line"] = line
        if language:
            query["Lang"] = language
        return self.call_api(
            "UpdateDomainRecord",
            queries=query
        )

    def delete_resource_record(self, aliyun_record_id: str):
        return self.call_api(
            "DeleteDomainRecord",
            {
                "RecordId": aliyun_record_id
            }
        )
