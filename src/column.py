from copy import deepcopy
from collections import Iterable


class Column(object):
    LEFT = 'l'
    RIGHT = 'r'
    DEFAULT_FORMAT = '{}'
    DEFAULTS = {
        'name': '',
        'display_name': '',
        'justified': LEFT,
        'format': '{}'
    }
    TRUE = 'x'
    FALSE = ''

    def __init__(self, config):
        c = deepcopy(self.DEFAULTS)
        c.update(config)

        if not c['display_name']:
            c['display_name'] = c['name']

        self.name = c['name']
        self.display_name = c['display_name']
        self.justified = c['justified']
        self.format_str = c['format']

        self.items = []
        self.width = len(self.display_name)

    def add(self, task):
        task_item = task.get(self.name)
        if task_item is not None:
            task_item = self._render_column_value(task_item)
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

    def _render_column_value(self, task_item):
        if isinstance(task_item, bool):
            return self.TRUE if task_item else self.FALSE
        elif isinstance(task_item, (int, float, str)):
            return self.format_str.format(task_item)
        elif isinstance(task_item, Iterable):
            return ','.join(task_item)
        else:
            return str(task_item)
