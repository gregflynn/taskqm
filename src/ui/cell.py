from src.util import Color
from src.settings import Settings, ColumnConfig


class Cell(object):
    def __init__(self, column_config, item):
        self.justify = column_config.justify
        self.format = column_config.fmt
        self.item = self._render_cell_value(item)

        column_colors = Settings.CELL_COLORS.get(column_config.name) or {}
        self._primary_color = column_colors.get(self.item)
        self._backup_color = column_colors.get(None)

    @property
    def width(self):
        return len(self.item)

    def render(self, width):
        padding = ' ' * (width - self.width)
        return (
            (padding if self.justify == ColumnConfig.RIGHT else '')
            + self._colorize()
            + (padding if self.justify == ColumnConfig.LEFT else '')
        )

    def _render_cell_value(self, item):
        if isinstance(item, bool):
            return Settings.TRUE if item else Settings.FALSE
        elif isinstance(item, (int, float, str)):
            return self.format.format(item)
        elif isinstance(item, (list, set)):
            return ','.join(item)
        else:
            return str(item)

    def _colorize(self):
        color = self._primary_color or self._backup_color
        if not color:
            return self.item

        if isinstance(color, str):
            return Color.paint(color, self.item)
        else:
            fg, bg = color
            return Color.paint(fg, bg, self.item)


class HeaderCell(Cell):
    def __init__(self, column_config):
        super().__init__(column_config, column_config.display_name)
        self._primary_color = Settings.THEME_COLOR

    def _render_cell_value(self, item):
        return item


class EmptyCell(Cell):
    @classmethod
    def render(cls, width):
        return ' ' * width


class DividerCell(Cell):
    @classmethod
    def render(cls, width):
        return Color.paint(Settings.THEME_COLOR, '-' * width)
