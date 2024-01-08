import base64
import json
import logging
from scrapy.http import HtmlResponse, JsonRequest
import scrapy

from scrapy import signals

# # useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter

logger = logging.getLogger(__name__)


class TutorialDownloaderMiddleware:
    _webapi_url = "https://api.webit.live/api/v1/realtime/web"

    def __init__(self, *, enabled, username, password):
        self._auth_credential = base64.b64encode(
            bytes(f"{username}:{password}", "utf-8")
        ).decode("utf-8")
        self._enabled = enabled

    @classmethod
    def from_crawler(cls, crawler):
        enabled = crawler.settings.getbool("NIMBLE_ENABLED")
        username = crawler.settings.get("NIMBLE_USERNAME") or ""
        password = crawler.settings.get("NIMBLE_PASSWORD") or ""

        return cls(enabled=enabled, username=username, password=password)

    def process_request(self, request, spider):
        if not self._enabled:
            return

        if request.headers.has_key("X-Nimble"):
            return

        headers = {
            "Authorization": f"Basic {self._auth_credential}",
            "Content-Type": "application/json",
            "X-Nimble": 1,
        }
        data = {
            "url": request.url,
            "render": True,
        }
        return scrapy.http.JsonRequest(
            self._webapi_url,
            method="POST",
            data=data,
            headers=headers,
            cb_kwargs=request.cb_kwargs,
            meta=request.meta,
        )

    def process_response(self, request, response, spider):
        if not self._enabled:
            return response

        nimble_response = response.json()
        new_response = response.replace(
            url=nimble_response["input_url"],
            status=nimble_response["status_code"],
            headers=nimble_response["headers"],
            body=nimble_response["html_content"],
        )

        return new_response
