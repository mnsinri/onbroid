import json

class Selector():
	def __init__(self):
		with open('./selector.json') as f:
			self.config = json.load(f)

	def term_path(self):
		return self.config.get('term_path')

	def term_path_jp(self):
		return self.config.get('term_path_jp')

	def term_detail_path(self):
		return self.config.get('term_detail_path')

	def term_meaning_path(self):
		return self.config.get('term_meaning_path')

	def catalog_container(self):
		return self.config.get('catalog_container')

	def legends_name(self):
		return self.config.get('legends_name')

	def legends_copy(self):
		return self.config.get('legends_copy')

	def legends_thumbnail(self):
		return self.config.get('legends_thumbnail')
	
	def legends_url(self):
		return self.config.get('legends_url')

	def legend_details(self):
		return self.config.get('legend_details')

	def legend_details_name(self):
		return self.config.get('legend_details_name')

	def legend_details_value(self):
		return self.config.get('legend_details_value')

