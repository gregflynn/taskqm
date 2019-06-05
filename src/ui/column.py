from src.settings import Settings


class Column(object):
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
