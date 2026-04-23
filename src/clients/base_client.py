import requests
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

MAX_BODY_LOG = 500


class BaseClient:
    def __init__(self, base_url: str, timeout: float = 10.0, session: requests.Session | None = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

        # --- retry

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)




    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        timeout = kwargs.pop("timeout", self.timeout)






        # --- request log ---
        logger.info(f"{method} {url}")

        if logger.isEnabledFor(logging.DEBUG):
            if "json" in kwargs:
                logger.debug(f"Request JSON: {kwargs['json']}")
            if "data" in kwargs:
                logger.debug(f"Request DATA: {kwargs['data']}")
            if "params" in kwargs:
                logger.debug(f"Query params: {kwargs['params']}")

        start_time = time.time()

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=timeout,
                **kwargs
            )
        except Exception as e:
            logger.exception(f"Request failed: {method} {url}")
            raise

        duration = time.time() - start_time

        # --- response log ---
        logger.info(f"Response {response.status_code} ({duration:.2f}s)")

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Response body: {response.text[:MAX_BODY_LOG]}")

        # --- log error ---
        if response.status_code >= 400:
            logger.error(
                f"HTTP {response.status_code} error: {response.text[:MAX_BODY_LOG]}"
            )

        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request("DELETE", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self._request("PUT", path, **kwargs)