class ColumnConfig(object):
    LEFT = 'l'
    RIGHT = 'r'

    def __init__(self, name, display_name=None, justify=None, fmt=None):
        if display_name is None:
            display_name = name

        self.name = name
        self.display_name = display_name
        self.justify = justify or self.LEFT
        self.fmt = fmt or '{}'
