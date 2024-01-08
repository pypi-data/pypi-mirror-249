import os

import httpx


class HangarScope:
    def __init__(
        self,
        region: str,
        name: str,
        roleAssumptions: list = [],
        api_key: str | None = None,
        _entity: str = None,
        endpoint: str = "https://api.tryhangar.com",
    ):
        if api_key is None:
            self.api_key = os.environ["HANGAR_API_KEY"]
        else:
            self.api_key = api_key

        if os.environ.get("HANGAR_URL") is not None:
            self.endpoint = os.environ["HANGAR_URL"]

        self.endpoint = endpoint
        self.region = region
        self.entity = _entity
        self.name = name
        # Maintained by api key
        self.roleAssumptions = roleAssumptions

    def add_construct(self, data, force_change=False):
        payload = {
            "region": self.region,
            "version": "v1",
            "roleAssumptions": self.roleAssumptions,
            "tags": [],
            "scope": self.name,
            **data,
            "forceChange": force_change,
        }
        try:
            if self.entity is not None:
                response = httpx.request(
                    "POST",
                    self.endpoint,
                    headers={"X-API-KEY": self.api_key},
                    json=payload,
                    timeout=20.0,
                )

            else:
                response = httpx.request(
                    "POST",
                    self.endpoint,
                    headers={"X-API-KEY": self.api_key},
                    json=payload,
                    timeout=20.0,
                )

        except httpx.ReadTimeout:
            raise Exception("Couldnt acquire lock")
        if response.status_code != 200:
            raise Exception(response.text)

        if "job_id" in response.json():
            return response.json()["job_id"]
        else:
            raise Exception(response.text)

    def get_logs(self, resource_id, path):
        res = httpx.request(
            "GET",
            self.endpoint + "/resources/" + resource_id + "/logs",
            headers={"X-API-KEY": self.api_key},
            params={"path": path},
        )

        return res.json()

    def get_state(self, resource_id):
        res = httpx.request(
            "GET",
            self.endpoint + "/state",
            headers={"X-API-KEY": self.api_key},
            params={
                "resourceId": resource_id,
            },
        )

        return res.json()[resource_id]

    def get_status(self, job_id):
        return httpx.request(
            "GET",
            self.endpoint + "/status",
            headers={"X-API-KEY": self.api_key},
            params={"job_id": job_id},
            timeout=httpx.Timeout(20.0),
        )

    def execute_action(self, resource_id, action: str, params={}):
        payload = {
            "resourceId": resource_id,
            "action": action,
            "params": params,
        }

        if self.entity is not None:
            response = httpx.request(
                "PATCH",
                self.endpoint,
                headers={"X-API-KEY": self.api_key},
                json=payload,
                params={"entityId": self.entity},
                timeout=20.0,
            )

        else:
            response = httpx.request(
                "PATCH",
                self.endpoint,
                headers={"X-API-KEY": self.api_key},
                json=payload,
                timeout=20.0,
            )

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()

    def delete_resource(self, resource_id):
        print("Deleting resource: " + resource_id)
        return httpx.request(
            "DELETE",
            self.endpoint,
            headers={"X-API-KEY": self.api_key},
            params={"resourceId": resource_id},
        )
