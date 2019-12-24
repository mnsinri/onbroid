import json

class Selector():
	def __init__(self):
		with open('./selector.json') as f:
			self.config = json.load(f)

	def main_path(self):
		return self.config.get('main_path')

	def term_path(self):
		return self.config.get('term_path')

	def meaning_path(self):
		return self.config.get('meaning_path')
