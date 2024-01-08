import base64

from scrapy.exceptions import NotConfigured
from scrapy.http import JsonRequest


class NimbleWebApiMiddleware:
    _webapi_url = "https://api.webit.live/api/v1/realtime/web"

    def __init__(self, *, enabled, username, password):
        self._auth_credential = base64.b64encode(
            bytes(f"{username}:{password}", "utf-8")
        ).decode("utf-8")
        self._enabled = enabled

    @classmethod
    def from_crawler(cls, crawler):
        enabled = crawler.settings.getbool("NIMBLE_ENABLED")
        if not enabled:
            raise NotConfigured("Missing NIMBLE_ENABLED setting.")

        username = crawler.settings.get("NIMBLE_USERNAME")
        if username is None:
            raise NotConfigured("Missing NIMBLE_USERNAME setting.")

        password = crawler.settings.get("NIMBLE_PASSWORD")
        if password is None:
            raise NotConfigured("Missing NIMBLE_PASSWORD setting.")

        return cls(enabled=enabled, username=username, password=password)

    def _get_request_options(self, request):
        # https://docs.nimbleway.com/data-platform/web-api/real-time-url-request#request-options
        request_options = {
            "url": request.url,
        }

        optional = [
            "method",
            "country",
            "locale",
            "headers",
            "cookies",
            "render",
            "render_options",
        ]
        for option in optional:
            key = f"nimble_{option}"
            if key in request.meta:
                request_options[option] = request.meta[key]

        return request_options

    def process_request(self, request, spider):
        if not self._enabled:
            return

        if request.headers.has_key("X-Nimble-Request"):
            return

        headers = {
            "Authorization": f"Basic {self._auth_credential}",
            "Content-Type": "application/json",
            "X-Nimble-Request": 1,
        }

        request_data = self._get_request_options(request)

        return JsonRequest(
            self._webapi_url,
            method="POST",
            data=request_data,
            headers=headers,
            cb_kwargs=request.cb_kwargs,
            meta=request.meta,
        )

    def process_response(self, request, response, spider):
        if not self._enabled:
            return response

        nimble_response = response.json()

        if nimble_response["status"] == "failed":
            return response

        new_response = response.replace(
            url=nimble_response["input_url"],
            status=nimble_response["status_code"],
            headers=nimble_response["headers"],
            body=nimble_response["html_content"],
        )

        return new_response
