import scrapy
from scrapy_splash import SplashRequest
import os


class JPGSpider(scrapy.Spider):
    name = "jpg"

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(**kwargs)
        self.url = url

    def start_requests(self):
        proxy = 'http://us-ca.proxymesh.com:31280'
        yield SplashRequest(
            self.url,
            callback=self.parse,
            endpoint='render.html',
            args={'wait': 5},
            meta={proxy: proxy}
        )

    def parse(self, response):
        image_url = response.css('img::attr(src)').get()
        folder_path = 'C:/Users/rules/PycharmProjects/pythonProject2/media/full/'
        file_names = os.listdir(folder_path)

        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)
        if image_url:
            yield {'image_urls': [image_url]}
