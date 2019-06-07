class BoardConfig(object):
    def __init__(self, name, query, columns, default=False, order='score-'):
        self.name = name
        self.query = query
        self.columns = columns
        self.default = default
        self.order = order
