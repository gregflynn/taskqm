from src.settings import Settings


class Column(object):
    PADDING = ' ' * Settings.PADDING

    def __init__(self, column_config):
        self.config = column_config
        self.items = []
        self.width = len(column_config.display_name)

    def add(self, task):
        task_item = task.get(self.config.name)
        if task_item is not None:
            task_item = self._render_column_value(task_item)
            self.width = max(self.width, len(task_item))
        self.items.append(task_item)

    def render(self, idx):
        return self._padded_fmt(self.items[idx])

    def header(self):
        return self._padded_fmt(self.config.display_name)

    def header_line(self):
        return '-' * self.width

    @property
    def size(self):
        return len(self.items)

    @staticmethod
    def build_column_group(tasks, columns=None):
        columns = [Column(c) for c in columns or Settings.COLUMNS]
        for task in tasks:
            for col in columns:
                col.add(task)
        return columns

    @classmethod
    def column_group_header(cls, columns):
        header_line = []
        divider = []
        for c in columns:
            header_line.append(c.header())
            divider.append(c.header_line())

        return '{}\n{}'.format(
            cls.PADDING.join(header_line), cls.PADDING.join(divider)
        )

    @classmethod
    def column_group_content(cls, columns):
        rendered_lines = []

        for idx in range(columns[0].size):
            rendered_cols = []

            for col in columns:
                rendered_cols.append(col.render(idx))

            rendered_lines.append(cls.PADDING.join(rendered_cols))

        return '\n'.join(rendered_lines)

    def _padded_fmt(self, item):
        if item is None:
            return ' ' * self.width
        padding = ' ' * (self.width - len(item))

        return (
            (padding if self.config.justify == self.config.RIGHT else '')
            + item
            + (padding if self.config.justify == self.config.LEFT else '')
        )

    def _render_column_value(self, task_item):
        if isinstance(task_item, bool):
            return Settings.TRUE if task_item else Settings.FALSE
        elif isinstance(task_item, (int, float, str)):
            return self.config.fmt.format(task_item)
        elif isinstance(task_item, (list, set)):
            return ','.join(task_item)
        else:
            return str(task_item)
