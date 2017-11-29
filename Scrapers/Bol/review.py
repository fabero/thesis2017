# bol.com review Spider
# By Lennart Faber
# 06-10-17

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from extruct.w3cmicrodata import MicrodataExtractor

class ReviewSpider(CrawlSpider):
	name = 'reviews'
	
	def __init__(self, url_file, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.url_file = url_file

	def start_requests(self):
		with open(self.url_file, 'r') as f:
			for url in f:
				url = url.strip()
				yield scrapy.Request(url, callback=self.parse)

	def parse(self, response):
		extractor = MicrodataExtractor()
		try:
			items = extractor.extract(response.body_as_unicode(),response.url)
			for item in items:
				if item.get('properties', {}).get('itemReviewed'):
					properties = item['properties']
					yield{
						'name': properties['itemReviewed'],
						'rating': properties['reviewRating']['properties']['ratingValue'],
						'reviewText': properties['description']
						}
		except:
			return