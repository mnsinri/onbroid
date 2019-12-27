import json

class Selector():
	def __init__(self):
		with open('./selector.json') as f:
			self.config = json.load(f)

	def term_path(self):
		return self.config.get('term_path')

	def term_detail_path(self):
		return self.config.get('term_detail_path')

	def term_meaning_path(self):
		return self.config.get('term_meaning_path')
