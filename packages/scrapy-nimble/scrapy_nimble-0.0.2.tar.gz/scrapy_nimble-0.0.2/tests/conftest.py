import pytest


@pytest.fixture
def middleware_settings():
    return {
        "NIMBLE_ENABLED": True,
        "NIMBLE_USERNAME": "username",
        "NIMBLE_PASSWORD": "password",
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_nimble.middlewares.NimbleWebApiMiddleware": 570,
        },
    }
