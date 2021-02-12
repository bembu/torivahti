# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from config import REGIONS, TYPES

from .parser import Parser

class ToriParser(Parser):
	"""
		A Parser for Tori.fi queries
	"""

	def __init__(self):
		super().__init__()
		self.location = "suomi"
		self.st="s" # --> Myydaan see a list of TYPES in config.py
		self.w="1" # --> Uusimaa see a list of REGIONS in config.py

		self.url = "http://tori.fi/{location}/?q={query}&st={st}&w={w}"



	def parse_html(self, html_doc):
		"""
			Parses the Tori.fi specific html
		"""
		soup = BeautifulSoup(html_doc.read(), features="html.parser")
		
		titles = {} # title as key, url as value

		for a in soup.findAll("a", attrs={"class": "item_row_flex"}):
			name = a.text.replace('\t', " ").replace("\n", " ").split()
			name = " ".join(name)
			href = a['href']
			titles[name] = href

		return titles

	def run(self, query):
		url = self.url.format(location=self.location, query=quote_plus(query,safe="*"), st=self.st, w=self.w)
		print('Searching for {}, of type {}, in region {}'.format(query,TYPES[self.st], REGIONS[self.w]))
		print(url)
		html_doc = self.query_data(url)
		data = self.parse_html(html_doc)

		diff = self.compare_to_local(query, data)

		self.mail_data[query] = diff
		self.mail_urls[query] = url

		if diff:
			return diff
			