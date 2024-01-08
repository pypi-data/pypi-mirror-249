import pytest
from scrapy.exceptions import NotConfigured
from scrapy.utils.test import get_crawler

from scrapy_nimble.middlewares import NimbleWebApiMiddleware


def test_not_configured_exception_if_enabled_setting_not_provided(middleware_settings):
    middleware_settings.pop("NIMBLE_ENABLED", None)

    with pytest.raises(NotConfigured):
        NimbleWebApiMiddleware.from_crawler(
            get_crawler(settings_dict=middleware_settings)
        )


def test_not_configured_exception_if_middleware_not_enabled(middleware_settings):
    middleware_settings["NIMBLE_ENABLED"] = False

    with pytest.raises(NotConfigured):
        NimbleWebApiMiddleware.from_crawler(
            get_crawler(settings_dict=middleware_settings)
        )


def test_not_configured_exception_if_username_setting_not_provided(middleware_settings):
    middleware_settings.pop("NIMBLE_USERNAME", None)

    with pytest.raises(NotConfigured):
        NimbleWebApiMiddleware.from_crawler(
            get_crawler(settings_dict=middleware_settings)
        )


def test_not_configured_exception_if_password_setting_not_provided(middleware_settings):
    middleware_settings.pop("NIMBLE_PASSWORD", None)

    with pytest.raises(NotConfigured):
        NimbleWebApiMiddleware.from_crawler(
            get_crawler(settings_dict=middleware_settings)
        )
