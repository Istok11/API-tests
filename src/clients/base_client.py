# import os
# import json
# import logging
# from typing import Optional, Any, Dict
#
# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
#
# from config import BASE_URL, TIMEOUT
#
# logger = logging.getLogger("qa_api")
#
#
# def _mask_headers(headers: Dict[str, str]) -> Dict[str, str]:
#     masked = dict(headers)
#     for k in list(masked.keys()):
#         if k.lower() in {"authorization", "x-api-key"}:
#             masked[k] = "***"
#     return masked
#
#
# class BaseClient:
#     def __init__(
#         self,
#         base_url: str = BASE_URL,
#         timeout: float = TIMEOUT,
#         token: Optional[str] = None,
#         retries_total: int = 3,
#         backoff_factor: float = 0.3,
#     ):
#         self.base_url = base_url.rstrip("/")
#         self.timeout = timeout
#         self.session = requests.Session()
#
#         # ---- Default headers (можно расширять)
#         self.session.headers.update({"Accept": "application/json"})
#
#         # ---- Auth (автоматически)
#         token = token or os.getenv("API_TOKEN")
#         if token:
#             self.session.headers.update({"Authorization": f"Bearer {token}"})
#
#         # ---- Retry (уровень транспорта)
#         retry = Retry(
#             total=retries_total,
#             connect=retries_total,
#             read=retries_total,
#             status=retries_total,
#             backoff_factor=backoff_factor,
#             status_forcelist=(429, 500, 502, 503, 504),
#             allowed_methods=("GET", "POST", "PUT", "PATCH", "DELETE"),
#             raise_on_status=False,  # не бросаем исключение, отдаём response
#         )
#         adapter = HTTPAdapter(max_retries=retry)
#         self.session.mount("http://", adapter)
#         self.session.mount("https://", adapter)
#
#     def _request(self, method: str, path: str, **kwargs) -> requests.Response:
#         url = f"{self.base_url}{path}"
#         timeout = kwargs.pop("timeout", self.timeout)
#
#         # Логируем запрос (маскируем секреты)
#         req_headers = {}
#         req_headers.update(self.session.headers)
#         req_headers.update(kwargs.get("headers", {}) or {})
#         safe_headers = _mask_headers({k: str(v) for k, v in req_headers.items()})
#
#         logger.info("HTTP %s %s", method, url)
#         if "params" in kwargs and kwargs["params"] is not None:
#             logger.info("Query params: %s", kwargs["params"])
#         logger.info("Headers: %s", safe_headers)
#
#         if "json" in kwargs and kwargs["json"] is not None:
#             logger.info("JSON body: %s", kwargs["json"])
#         elif "data" in kwargs and kwargs["data"] is not None:
#             logger.info("Data body: %s", kwargs["data"])
#
#         resp = self.session.request(method, url, timeout=timeout, **kwargs)
#
#         # Логируем ответ
#         logger.info("Response %s (%s)", resp.status_code, resp.headers.get("Content-Type", ""))
#         # Опционально: тело ответа (осторожно, может быть большое)
#         try:
#             if "application/json" in (resp.headers.get("Content-Type") or ""):
#                 logger.info("Response JSON: %s", resp.json())
#             else:
#                 text = resp.text
#                 logger.info("Response text (first 500): %s", text[:500])
#         except Exception:
#             logger.info("Response body: <unreadable>")
#
#         return resp
#
#     def get(self, path: str, **kwargs) -> requests.Response:
#         return self._request("GET", path, **kwargs)
#
#     def post(self, path: str, **kwargs) -> requests.Response:
#         return self._request("POST", path, **kwargs)
#
#     def put(self, path: str, **kwargs) -> requests.Response:
#         return self._request("PUT", path, **kwargs)
#
#     def patch(self, path: str, **kwargs) -> requests.Response:
#         return self._request("PATCH", path, **kwargs)
#
#     def delete(self, path: str, **kwargs) -> requests.Response:
#         return self._request("DELETE", path, **kwargs)
