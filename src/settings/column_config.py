class ColumnConfig(object):
    LEFT = 'l'
    RIGHT = 'r'

    def __init__(self, name, display_name=None, justify=None, fmt=None):
        if display_name is None:
            display_name = name[0] if isinstance(name, tuple) else name

        self.name = name
        self.display_name = display_name
        self.justify = justify or self.LEFT
        self.fmt = fmt or '{}'

    @property
    def is_composite_column(self):
        return isinstance(self.name, tuple)
