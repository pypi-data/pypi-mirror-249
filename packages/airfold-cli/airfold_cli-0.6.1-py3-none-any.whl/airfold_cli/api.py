import json
import os
from typing import Dict, List, Optional, Union

import requests
from airfold_common.project import ProjectFile
from requests import JSONDecodeError, PreparedRequest, Response
from requests.auth import AuthBase
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)
from typing_extensions import Self

from airfold_cli.error import (
    APIError,
    ConflictError,
    ForbiddenError,
    InternalServerError,
    ProjectNotFoundError,
    UnauthorizedError,
)
from airfold_cli.models import (
    Command,
    Config,
    OutputDataFormat,
    ProjectProfile,
    UserProfile,
)
from airfold_cli.utils import load_config

AIRFOLD_API_URL = "https://api.airfold.co"

RETRY_TIMES = 3
WAIT_MIN_SECONDS = 0.5
WAIT_MAX_SECONDS = 5


def api_retry(func):
    def wrapper(*args, **kwargs):
        return Retrying(
            retry=retry_if_exception_type(ConflictError),
            stop=stop_after_attempt(max_attempt_number=RETRY_TIMES),
            reraise=True,
            wait=wait_random_exponential(multiplier=1, min=WAIT_MIN_SECONDS, max=WAIT_MAX_SECONDS),
        )(func, *args, **kwargs)

    return wrapper


class BearerAuth(AuthBase):
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, req: PreparedRequest) -> PreparedRequest:
        req.headers["authorization"] = "Bearer " + self.token
        return req


class AirfoldApi:
    def __init__(self, api_key: str = "", endpoint: str = ""):
        self.auth: AuthBase = BearerAuth(api_key)
        self.endpoint: str = endpoint or os.environ.get("AIRFOLD_API_URL", AIRFOLD_API_URL)
        self.identity: Union[UserProfile, ProjectProfile] | None = None

    @classmethod
    def from_config(cls, _config: Config | None = None) -> Self:
        config: Config = _config or load_config()
        return cls(api_key=config.key, endpoint=config.endpoint)

    def _get_identity(self) -> Response:
        return requests.get(self.endpoint + "/v1/auth/identity", auth=self.auth)

    @api_retry
    def get_identity(self) -> Union[ProjectProfile, UserProfile]:
        res = self._get_identity()
        if res.ok:
            json_data = res.json()
            if json_data.get("user"):
                return UserProfile(**json_data.get("user"))
            else:
                return ProjectProfile(**json_data)

        raise self._resp_to_err(res)

    def init_identity(self) -> None:
        if not self.identity:
            self.identity = self.get_identity()

    def get_org_id(self) -> str:
        self.init_identity()
        assert self.identity is not None
        if isinstance(self.identity, UserProfile):
            return self.identity.organizations[0].id
        return self.identity.org_id

    @api_retry
    def list_projects(self, org_id: Optional[str] = None) -> Response:
        return requests.get(self.endpoint + f"/v1/{org_id or self.get_org_id()}/projects", auth=self.auth)

    @staticmethod
    def parse_error_response(res: Response) -> str:
        try:
            data: Dict = res.json()
            if data.get("error"):
                return data["error"]
            return res.reason
        except JSONDecodeError:
            pass
        if len(res.text) > 0 and res.status_code == 500:
            return res.text
        return res.reason

    def _resp_to_err(self, res: Response) -> APIError:
        desc = self.parse_error_response(res)
        if res.status_code == 401:
            return UnauthorizedError(desc)
        elif res.status_code == 403:
            return ForbiddenError(desc)
        elif res.status_code == 404:
            return ProjectNotFoundError(desc)
        elif res.status_code == 409:
            return ConflictError(desc)
        elif res.status_code >= 500:
            return InternalServerError(desc)
        return APIError(desc)

    def _project_push(
        self,
        data: str,
        dry_run: bool,
        force: bool,
    ) -> Response:
        url = self.endpoint + f"/v1/push"
        params = {"dry_run": dry_run, "force": force}
        headers = {"Content-Type": "application/yaml"}
        response = requests.post(url, data=data, params=params, headers=headers, auth=self.auth)

        return response

    @api_retry
    def project_push(
        self,
        data: str,
        dry_run: bool = False,
        force: bool = False,
    ) -> List[Command]:
        res = self._project_push(data, dry_run, force)
        if res.ok:
            return [Command(**cmd) for cmd in res.json()]
        raise self._resp_to_err(res)

    def _project_pull(
        self,
    ) -> Response:
        return requests.get(self.endpoint + f"/v1/pull", auth=self.auth)

    @api_retry
    def project_pull(
        self,
    ) -> List[ProjectFile]:
        res = self._project_pull()
        if res.ok:
            return [ProjectFile(name=data["name"], data=data, pulled=True) for data in res.json()]  # type: ignore
        raise self._resp_to_err(res)

    def _project_graph(
        self,
    ) -> Response:
        return requests.get(self.endpoint + f"/v1/graph", auth=self.auth)

    @api_retry
    def project_graph(
        self,
    ) -> Dict:
        res = self._project_graph()
        if res.ok:
            return res.json()
        raise self._resp_to_err(res)

    def _project_pipe_delete(self, name: str, dry_run: bool, force: bool) -> Response:
        params = {"dry_run": dry_run, "force": force}
        return requests.delete(
            self.endpoint + f"/v1/pipes/{name}",
            params=params,
            auth=self.auth,
        )

    @api_retry
    def project_pipe_delete(self, name: str, dry_run: bool = False, force: bool = False) -> List[Command]:
        res = self._project_pipe_delete(name, dry_run, force)
        if res.ok:
            return [Command(**cmd) for cmd in res.json()]
        raise self._resp_to_err(res)

    def _project_source_delete(self, name: str, dry_run: bool, force: bool) -> Response:
        params = {"dry_run": dry_run, "force": force}
        return requests.delete(
            self.endpoint + f"/v1/sources/{name}",
            params=params,
            auth=self.auth,
        )

    @api_retry
    def project_source_delete(self, name: str, dry_run: bool = False, force: bool = False) -> List[Command]:
        res = self._project_source_delete(name, dry_run, force)
        if res.ok:
            return [Command(**cmd) for cmd in res.json()]
        raise self._resp_to_err(res)

    def _project_pipe_get_data(self, name: str, format: OutputDataFormat) -> Response:
        return requests.get(
            self.endpoint + f"/v1/pipes/{name}.{format}",
            auth=self.auth,
        )

    @api_retry
    def project_pipe_get_data(self, name: str, format: OutputDataFormat = OutputDataFormat.NDJSON) -> List[Dict]:
        res = self._project_pipe_get_data(name, format)
        if res.ok:
            if format == OutputDataFormat.JSON:
                return [res.json()]

            ndjson_lines = res.text.split("\n")
            parsed_json = []
            for line in ndjson_lines:
                if line:
                    json_object = json.loads(line)
                    parsed_json.append(json_object)

            return parsed_json
        raise self._resp_to_err(res)

    def _rename(self, url_path: str, new_name: str, dry_run: bool, force: bool) -> Response:
        params: dict[str, bool | str] = {"new_name": new_name, "dry_run": dry_run, "force": force}
        return requests.post(
            self.endpoint + url_path,
            params=params,
            auth=self.auth,
        )

    @api_retry
    def rename_source(self, name: str, new_name: str, dry_run: bool = False, force: bool = False) -> List[Command]:
        res = self._rename(f"/v1/sources/{name}", new_name, dry_run, force)
        if res.ok:
            return [Command(**cmd) for cmd in res.json()]
        raise self._resp_to_err(res)

    @api_retry
    def rename_pipe(self, name: str, new_name: str, dry_run: bool = False, force: bool = False) -> List[Command]:
        res = self._rename(f"/v1/pipes/{name}", new_name, dry_run, force)
        if res.ok:
            return [Command(**cmd) for cmd in res.json()]
        raise self._resp_to_err(res)
