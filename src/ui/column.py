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

    def render(self, row_num, line_num):
        return self.cells[row_num].render(self.width, line_num)

    @property
    def rows(self):
        return len(self.cells)

    def row_height(self, row_num):
        return self.cells[row_num].height


class ColumnGroup(object):
    PADDING = ' ' * Settings.PADDING

    def __init__(self, tasks, column_configs):
        self.columns = [Column(c) for c in column_configs]
        for task in tasks:
            for col in self.columns:
                col.add(task)

    @property
    def rows(self):
        return self.columns[0].rows

    def render(self, header=True):
        rendered_lines = []

        for row_num in range(self.rows):
            if not header and row_num < 2:
                continue

            cell_lines = max(c.row_height(row_num) for c in self.columns)

            for line_num in range(cell_lines):
                rendered_cols = []

                for col in self.columns:
                    rendered_cols.append(col.render(row_num, line_num))

                rendered_lines.append(self.PADDING.join(rendered_cols))

        return '\n'.join(rendered_lines)
