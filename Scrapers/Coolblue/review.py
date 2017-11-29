# Coolblue review Spider
# By Lennart Faber
# 06-10-17

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

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
		for review in response.css('li.reviews__list-item.js-review'):
			yield {
				'url':response.url,
				'title':response.css('h3.h4.review--header-title ::text').extract_first().strip()[1:-1],
				'rating':response.css('.review--header-rating ::text').extract_first().strip().split('/')[0],
				'text': response.css('.review--description.js-review-description ::text').extract_first().strip(),
				'votes-up': response.css('.review--counter.js-review-vote-up ::text').extract_first(),
				'votes-down':response.css('.review--counter.js-review-vote-down ::text').extract_first()
			}

			