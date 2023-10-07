import scrapy
from scrapy_splash import SplashRequest


class JPGSpider(scrapy.Spider):
    name = "jpg"

    def __init__(self, url=None, *args, **kwargs):
        super().__init__(**kwargs)
        self.url = url

    def start_requests(self):
        yield SplashRequest(
            self.url,
            callback=self.parse,
            endpoint='render.html',
            args={'wait': 5},
        )

    def parse(self, response):
        image_url = response.css('img::attr(src)').get()
        if image_url:
            yield SplashRequest(
                image_url,
                callback=self.save_image,
                endpoint='render.png',
                args={'wait': 5},
            )

    def save_image(self, response):
        filename = 'C://Users//rules//PycharmProjects//pythonProject2//main_page//static//pictures//image.jpg'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Image saved as %s' % filename)
