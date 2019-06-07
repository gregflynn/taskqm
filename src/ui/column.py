from src.settings import Settings
from .cell import Cell, HeaderCell, DividerCell, EmptyCell


class Column(object):
    def __init__(self, column_config):
        self.config = column_config
        self.cells = [HeaderCell(column_config), DividerCell]
        self.width = len(column_config.display_name)

    def add(self, task):
        task_item = task.get(self.config.name)
        cell = None

        if task_item is None:
            cell = EmptyCell
        else:
            cell = Cell(self.config, task_item)
            self.width = max(self.width, cell.width)

        self.cells.append(cell)

    def render(self, idx):
        return self.cells[idx].render(self.width)

    def header(self):
        return self._header_cell.render(self.width)

    def header_line(self):
        return '-' * self.width

    @property
    def rows(self):
        return len(self.cells)


class ColumnGroup(object):
    PADDING = ' ' * Settings.PADDING

    def __init__(self, tasks, column_configs):
        self.columns = [Column(c) for c in column_configs]
        for task in tasks:
            for col in self.columns:
                col.add(task)

    def render(self, header=True):
        rendered_lines = []

        for idx in range(self.columns[0].rows):
            if not header and idx < 2:
                continue

            rendered_cols = []

            for col in self.columns:
                rendered_cols.append(col.render(idx))

            rendered_lines.append(self.PADDING.join(rendered_cols))

        return '\n'.join(rendered_lines)
