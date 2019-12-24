class Embed():

    # @params contents = {
    #   title,
    #   description,
    #   color,
    #   field : {
    #     name,
    #     value,
    #     inline
    #   },
    #   footer,
    # }
    def __init__(self, contents):
        self.title = contents.get('title')
        self.description = contents.get('description')
        self.color = contents.get('color', 0xff80c0)
        self.footer = contents.get('footer')
        self.field = contents.get('field')
        if self.field:
            self.field_name = self.field.get('name')
            self.field_value = self.field.get('value')
            self.field_inline = self.field.get('inline')
    
