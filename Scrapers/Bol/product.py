# bol.com product Spider
# By Lennart Faber
# 06-10-17

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ProductSpider(CrawlSpider):
	name = 'products'
	# this should be an url of the first page of a product category
	start_urls = ["https://www.bol.com/nl/l/digitale-camera-s/N/4070/?promo=digitale-fotografie_360__A_22612-22618-alle-fotocamera%27s_1_"]
	allowed_domains= ["bol.com"]
	rules = [
		Rule(
			LinkExtractor(
				allow='/nl/p/(.+)/(.+)/?suggestionType=browse',
				restrict_css = '#js_items_content'),
			callback = 'parse_product'),
		Rule(
			LinkExtractor(
				allow='page=(\d+)',
				restrict_css = '.pagination'))
		]

	def parse_product(self, response):
		# This might be a bit ugly, but it works
		reviews_url = "https://www.bol.com/nl/rnwy/productPage/reviews.html?productId=" + response.url.split('/')[-2] + "&offset=1&limit=10000"
		return {
			'product_name': response.css('.pdp-header__title.bol_header ::text').extract_first(),
			'reviews_url': reviews_url
		}