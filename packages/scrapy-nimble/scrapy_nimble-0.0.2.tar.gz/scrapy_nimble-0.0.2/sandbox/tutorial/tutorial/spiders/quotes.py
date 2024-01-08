import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["http://quotes.toscrape.com/"]

    def start_requests(self):
        yield scrapy.Request(
            "http://quotes.toscrape.com/js/",
            meta={
                "nimble_country": "DE",
                "nimble_locale": "pt",
                "nimble_render": True,
            },
        )

    def parse(self, response):
        for quote in response.css(".quote"):
            yield {
                "quote": quote.css(".text::text").get(),
                "author": quote.css(".author::text").get(),
            }

        # yield scrapy.Request(
        #     response.urljoin(response.css(".next a::attr(href)").get()),
        #     meta={'test_meta': 'content'}
        # )


class PhoneSpider(scrapy.Spider):
    name = "phones"

    def start_requests(self):
        # yield scrapy.Request("https://api.whatsapp.com/send?phone=598")
        phone_range = [number for number in range(93_330_000, 93_331_000)]
        # phone_range = [
        #     93330001,
        # ]
        for number in phone_range:
            yield scrapy.Request(
                f"https://api.whatsapp.com/send?phone=598{number}",
                cb_kwargs={"phone_number": f"598{number}"},
            )

    def parse(self, response, phone_number):
        yield {
            "url": response.url,
            "phone_number": phone_number,
            "title": response.xpath('//meta[@property="og:title"]/@content').get(),
            "image_url": response.xpath('//meta[@property="og:image"]/@content').get(),
            "type": response.xpath('//meta[@property="og:description"]/@content').get(),
        }

# Matrix
# EsU7 p65Z XDMy 1ZB7 Ffqm kzH5 PGHz EnP7 yXyh C75v tnt1 UNTP