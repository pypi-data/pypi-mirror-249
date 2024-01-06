import functools
from base64 import b64encode
from typing import TypedDict

import requests
from nacl import encoding, public


class RepoPublicKey(TypedDict):
    key_id: str
    key: str


def secret_encrypt(public_key: str, secret_value: str) -> str:
    """
    https://docs.github.com/en/rest/actions/secrets?apiVersion=2022-11-28#create-or-update-a-repository-secret
    :param public_key:
    :param secret_value:
    :return:
    """
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder)
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


class GithubClient:
    def __init__(self, api="https://api.github.com"):
        self.api = api
        self.gh_headers = {
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        }
        self.session = requests.session()

    @functools.lru_cache(maxsize=256)
    def authenticated_headers(self, token):
        headers = {k: v for k, v in self.gh_headers.items()}
        headers["Authorization"] = f"Bearer {token}"
        return headers

    def login_via_pat(self, token):
        self.session.headers = self.authenticated_headers(token)

    def login_via_gh_app(self):
        raise NotImplementedError

    def request(self, method, path, *args, **kwargs):
        _req = self.session.request(method, f"{self.api}/{path}", *args, **kwargs)
        match _req.status_code:
            case 200:
                return _req.json()
            case 204:
                return True
            case _:
                data = _req.json()
                raise Exception(f"{data['message']}: {data['documentation_url']}")

    def read(self, path, *args, **kwargs):
        return self.request("GET", path, *args, **kwargs)

    def list_organization_secrets(self, org_name):
        return self.read(f"orgs/{org_name}/actions/secrets")

    def list_repo_secrets(self, owner, repo_name):
        return self.read(f"repos/{owner}/{repo_name}/actions/secrets")

    @functools.lru_cache(maxsize=256)
    def get_repo_public_key(self, owner, repo_name) -> RepoPublicKey:
        return self.read(f"repos/{owner}/{repo_name}/actions/secrets/public-key")

    def get_repo_secret(self, owner, repo_name, secret_name):
        return self.read(f"repos/{owner}/{repo_name}/actions/secrets/{secret_name}")

    def delete_repo_secrets(self, owner, repo_name, secret_name):
        return self.request("DELETE", f"repos/{owner}/{repo_name}/actions/{secret_name}")

    def put_repo_secrets(self, owner, repo_name, secret_name, data, encrypted_key_id, public_key) -> bool:
        encrypted_value = secret_encrypt(public_key, data)
        return self.request("PUT", f"repos/{owner}/{repo_name}/actions/secrets/{secret_name}", json={
            "encrypted_value": encrypted_value,
            "key_id": encrypted_key_id
        })

    def set_repo_secret(self, owner, repo_name, secret_name, secret_value) -> bool:
        public_key = self.get_repo_public_key(owner, repo_name)
        return self.put_repo_secrets(owner, repo_name, secret_name, secret_value, public_key['key_id'], public_key['key'])
