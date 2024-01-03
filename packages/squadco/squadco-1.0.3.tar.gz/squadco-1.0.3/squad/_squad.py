import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from squad.utils.exceptions import SquadError,InvalidSecretKey
from squad.utils.types import JSONDict
from squad.utils.logging import get_logger

_LOGGER = get_logger(__name__, class_name="SquadRequest")


class SquadState:
    """making class attributes global"""

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class SquadClient(SquadState):
    """represents a client for interacting with the Squad API"""

    def __init__(self, **kwargs):
        SquadState.__init__(self)
        secret_key = kwargs.get("secret_key")
        if not hasattr(self, 'requests'):
            req = SquadRequest(headers={"Authorization": f"Bearer {secret_key}"}, test=kwargs.get("test"))
            self._shared_state.update(requests=req)


class SquadRequest(object):
    def __init__(self, headers=None,test=True):
        self.test = test
        self._API_BASE_URL = "https://sandbox-api-d.squadco.com" if test else "https://api-d.squadco.com"
        self.headers = headers
        self.request_timeout = 120
        self.session = requests.Session()
        retries = Retry(
            total=4,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _send_request(self, endpoint: str, method="get", **kwargs):
        """
        The function sends a request to an endpoint.
        """
        data = kwargs.get("data")

        payload = self._request_wrapper(
            url=self._API_BASE_URL + endpoint,
            method=method,
            request_data=data,
            headers=self.headers,
        )
        return payload

    def _request_wrapper(self, url, method, headers, request_data=None):
        try:
            if method.lower() == "get":
                response = self.session.get(url, headers=headers, params=request_data)
            elif method.lower() == "post":
                response = self.session.post(url, headers=headers, json=request_data)
            elif method.lower() == "patch":
                response = self.session.patch(url, headers=headers, json=request_data)
            elif method.lower() == "delete":
                response = self.session.delete(url, headers=headers, params=request_data)

            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 403:
                raise InvalidSecretKey(f"Invalid secret_key for {'test' if self.test else 'live'} mode")
            else:
                
                return err.response.json()
        except requests.exceptions.RequestException as e:
            return e.response.json()

    @staticmethod
    def parse_json_payload(payload: bytes) -> JSONDict:
        decoded_s = payload.decode("utf-8", "replace")
        try:
            return json.loads(decoded_s)
        except ValueError as exc:
            _LOGGER.error('Can not load invalid JSON data: "%s"', decoded_s)
            raise SquadError("Invalid server response") from exc
