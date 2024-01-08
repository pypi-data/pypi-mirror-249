# Scrapy Nimble Middleware

`scrapy-nimble` is a [Scrapy Downloader Middleware](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html) that helps to integrate
[Scrapy](https://scrapy.org) with [Nimble Web API](https://nimbleway.com/nimble-api/web/).

## Install

You can install `scrapy-nimble` as a regular Python package from
[PyPI](https://pypi.org/) using:

```shell
pip install scrapy-nimble
```

## Configuration

1. If you don't have it yet, [open an account](https://nimbleway.com/contact/) with [Nimble](https://nimbleway.com/).

1. Provide your credentials and enable the middleware through Scrapy settings.

   ```python
   # settings.py
   NIMBLE_ENABLED = True

   NIMBLE_USERNAME = "username"
   NIMBLE_PASSWORD = "password"
   ```

1. Add the downloader middleware to your `DOWNLOADER_MIDDLEWARES` Scrapy setting.

   ```python
   # settings.py
   DOWNLOADER_MIDDLEWARES = {
       "scrapy_nimble.middlewares.NimbleWebApiMiddleware": 570,
   }
   ```

   If you have `scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware` enabled
   (it is enabled by default in [DOWNLOADER_MIDDLEWARES_BASE](https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-DOWNLOADER_MIDDLEWARES_BASE)
   setting with default order equal to 590), configure `scrapy-nimble` middleware **before** it.

## Basic Usage

Once the downloader middleware is properly configured, every request goes through the Nimble's Web API.
There is no need to change anything in your spider's code.

## Real-time URL request

`scrapy-nimble` uses [Nimble Web API](https://docs.nimbleway.com/data-platform/web-api) with Real-time URL
requests. In addition to the default GET request for a specific URL, this API provides some extra options
that allow you to execute geolocated requests, render dynamic content, among others.

Right now the following [request options](https://docs.nimbleway.com/data-platform/web-api/real-time-url-request#request-options) can be used. Check the documentation for usage and the valid values that can be provided.
If the option is not given, the default value from Web API will be used.

- `method`
- `country`
- `locale`
- `headers`
- `cookies`
- `render`
- `render_options`

Add the options you want to be used inside the `meta` key of your request, appending `nimble_` to the
option name such as:

   ```python
   # Inside your spider
   yield scrapy.Request(
      "https://nimbleway.com",
      meta={
         "nimble_country": "DE",
         "nimble_locale": "uk",
         "nimble_render": True,
      }
   )
   ```

## Development

We suggest the use of [pyenv](https://github.com/pyenv/pyenv) to manage your Python version and create an isolated
environment where you can safely develop. After installing it, you can prepare the environment using the following
commands:

   ```bash
   $ pyenv virtualenv 3.11.6 myvenv
   $ pyenv activate myvenv
   $ python -m pip install -e .
   ```

To keep a standard in code formatting and do some linter checks, we use [pre-commit hooks](https://pre-commit.com/).
[Install](https://pre-commit.com/#installation) `pre-commit` package and install the project hooks using:

   ```bash
   $ pre-commit install
   ```

Now you are ready to start development.
