from src.util import Color
from src.settings import Settings, ColumnConfig


class Cell(object):
    def __init__(self, column_config, item):
        self.justify = column_config.justify
        self.format = column_config.fmt
        self.item = self._render_cell_value(item)

        column_colors = Settings.CELL_COLORS.get(column_config.name) or {}
        self._primary_color = column_colors.get(self.item[0])
        self._backup_color = column_colors.get(None)
        self.width = max(len(l) for l in self.item)
        self.height = len(self.item)

    def render(self, width, line_num):
        line = self.item[line_num] if line_num < self.height else ''
        padding = ' ' * (width - len(line))
        return (
            (padding if self.justify == ColumnConfig.RIGHT else '')
            + self._colorize(line)
            + (padding if self.justify == ColumnConfig.LEFT else '')
        )

    def _render_cell_value(self, item):
        if isinstance(item, bool):
            return [Settings.TRUE if item else Settings.FALSE]
        elif isinstance(item, (int, float)):
            return [self.format.format(item)]
        elif isinstance(item, (list, set)):
            return [','.join(item)]
        else:
            return str(item).split('\n')

    def _colorize(self, line):
        color = self._primary_color or self._backup_color
        if not color:
            return line

        if isinstance(color, str):
            return Color.paint(color, line)
        else:
            fg, bg = color
            return Color.paint(fg, bg, line)


class HeaderCell(Cell):
    def __init__(self, column_config):
        super().__init__(column_config, column_config.display_name)
        self._primary_color = Settings.THEME_COLOR

    def _render_cell_value(self, item):
        return [item]


class EmptyCell(Cell):
    height = 1

    @classmethod
    def render(cls, width, line_num):
        return ' ' * width


class DividerCell(EmptyCell):
    @classmethod
    def render(cls, width, line_num):
        return Color.paint(Settings.THEME_COLOR, '-' * width)
