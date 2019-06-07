from src.settings import Settings, ColumnConfig


class Cell(object):
    def __init__(self, column_config, item):
        self.config = column_config
        self.item = self._render_cell_value(item)

    @property
    def width(self):
        return len(self.item)

    def render(self, width):
        padding = ' ' * (width - self.width)
        return (
            (padding if self.config.justify == ColumnConfig.RIGHT else '')
            + self.item
            + (padding if self.config.justify == ColumnConfig.LEFT else '')
        )

    def _render_cell_value(self, item):
        if isinstance(item, bool):
            return Settings.TRUE if item else Settings.FALSE
        elif isinstance(item, (int, float, str)):
            return self.config.fmt.format(item)
        elif isinstance(item, (list, set)):
            return ','.join(item)
        else:
            return str(item)


class HeaderCell(Cell):
    def __init__(self, column_config):
        super().__init__(column_config, column_config.display_name)

    def _render_cell_value(self, item):
        return item


class EmptyCell(Cell):
    @classmethod
    def render(cls, width):
        return ' ' * width


class DividerCell(Cell):
    @classmethod
    def render(cls, width):
        return '-' * width
