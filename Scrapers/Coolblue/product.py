# Coolblue product Spider
# By Lennart Faber
# 06-10-17

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class ProductSpider(CrawlSpider):
	name = 'products'
	start_urls = ["https://www.coolblue.nl/producttype:mobiele-telefoons"]
	allowed_domains= ["coolblue.nl"]
	rules = [
		Rule(
			LinkExtractor(
				allow='/product/(.+)',
				restrict_css = '.product-grid.js-products'),
			callback = 'parse_product'),
		Rule(
			LinkExtractor(
				allow='pagina=(\d+)',
				restrict_css = '.pagination.js-pagination'))
		]

	def parse_product(self, response):
		try:
			reviews_count = int(response.css('.review-rating--reviews ::text').extract()[4].strip().split(' ')[0])
		except ValueError:
			reviews_count = 0
		return {
			'product_name': response.css('.js-product-name ::text').extract_first().strip(),
			'reviews_url': response.css('.review-rating--reviews a::attr(href)').extract_first(),
			'reviews_count': reviews_count
		}