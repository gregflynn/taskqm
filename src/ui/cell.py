from src.util import Color
from src.settings import Settings, ColumnConfig


class Cell(object):
    def __init__(self, column_config, item):
        self.justify = column_config.justify
        self.format = column_config.fmt
        item_key = item[0] if isinstance(item, (list, tuple)) else item

        column_colors = Settings.CELL_COLORS.get(column_config.name) or {}
        self._primary_color = column_colors.get(item_key)
        self._backup_color = column_colors.get(None)

        replacements = Settings.CELL_REPLACEMENTS.get(column_config.name) or {}
        self.item = self._render_cell_value(replacements.get(item_key, item))

        self.width = max(len(l) for l in self.item)
        self.height = len(self.item)

    def render(self, width, line_num):
        line = self.item[line_num] if line_num < self.height else ''
        padding = ' ' * (width - len(line))
        return (
            (padding if self.justify == ColumnConfig.RIGHT else '')
            + (self._colorize(line) if line else '')
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


class CompositeCell(object):
    PADDING = 0

    def __init__(self, column_config, items):
        self.justify = column_config.justify
        self.cells = []
        self.width = 0
        self.height = 1

        for idx, item in enumerate(items):
            name = column_config.name[idx]
            config = ColumnConfig(name)

            if item is None:
                continue

            cell = Cell(config, item)

            self.cells.append(cell)
            if cell.width > 0:
                self.width += (cell.width + self.PADDING)
                self.height = max(self.height, cell.height)

        self.width = max(self.width - self.PADDING, 0)

    def render(self, width, line_num):
        line_parts = []
        line_width = 0

        for cell in self.cells:
            cell_render = cell.render(0, line_num)

            if cell_render:
                line_parts.append(cell_render)
                line_width += cell.width

        line = (' ' * self.PADDING).join(line_parts)
        line_width += max((len(line_parts) * self.PADDING - 1), 0)

        padding = ' ' * (width - line_width)
        return (
            (padding if self.justify == ColumnConfig.RIGHT else '')
            + line
            + (padding if self.justify == ColumnConfig.LEFT else '')
        )


class HeaderCell(Cell):
    def __init__(self, column_config):
        super().__init__(column_config, column_config.display_name)
        self._primary_color = Settings.THEME_COLOR

    def _render_cell_value(self, item):
        return [item]


class EmptyCell(Cell):
    height = 1
    width = 0

    @classmethod
    def render(cls, width, line_num):
        return ' ' * width


class DividerCell(EmptyCell):
    @classmethod
    def render(cls, width, line_num):
        return Color.paint(Settings.THEME_COLOR, '-' * width)
