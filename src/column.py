from collections import Iterable


class Column(object):
    LEFT = 'l'
    RIGHT = 'r'
    DEFAULT_FORMAT = '{}'

    def __init__(self, name):
        """
        Args:
            name (str|tuple): name of the column, or:
                (0 name of the column
                (1) display name of the column
                [2] l/r justified
                [3] format string
        """
        if isinstance(name, str):
            self.name = name
            self.display_name = name
            self.justified = self.LEFT
            self.format_str = self.DEFAULT_FORMAT
        else:
            self.name = name[0]
            self.display_name = name[1]
            self.justified = name[2] if len(name) > 2 else self.LEFT
            self.format_str = name[3] if len(name) > 3 else self.DEFAULT_FORMAT

        self.items = []
        self.width = len(self.display_name)

    def add(self, task):
        task_item = task.get(self.name)
        if task_item is not None:
            if (
                isinstance(task_item, Iterable)
                and not isinstance(task_item, str)
            ):
                task_item = ','.join(task_item)
            elif isinstance(task_item, (int, float)):
                task_item = self.format_str.format(task_item)
            else:
                task_item = str(task_item)
            self.width = max(self.width, len(task_item))
        self.items.append(task_item)

    def render(self, idx):
        return self._padded_fmt(self.items[idx])

    def header(self):
        return self._padded_fmt(self.display_name)

    def header_line(self):
        return '-' * self.width

    def _padded_fmt(self, item):
        if item is None:
            return ' ' * self.width
        padding = ' ' * (self.width - len(item))

        return (
            (padding if self.justified == self.RIGHT else '')
            + item
            + (padding if self.justified == self.LEFT else '')
        )
