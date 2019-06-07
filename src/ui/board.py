from src.services import TaskService
from src.settings import Settings
from .column import ColumnGroup


class Board(object):
    def __init__(self, name, query):
        self.name = name
        self.query = query
        self._col_map = {c.display_name: c.name for c in Settings.COLUMNS}

    def count(self):
        return len(TaskService.get_tasks(query=self.query))

    def render(self, filters, order):
        tasks = self._get_sorted_tasks(filters, order)
        print(ColumnGroup(tasks).render())

    def _get_sorted_tasks(self, filters, order):
        tasks = TaskService.get_tasks(query=f'{self.query} {filters}')

        for o, directon in reversed(self._parse_order(order)):
            key = self._col_map.get(o) or o
            tasks = sorted(
                tasks, key=lambda t: t.get(key), reverse=directon == '-'
            )

        return tasks

    def _parse_order(self, order):
        orders = []
        ops = {'+', '-'}

        for o in order.split(','):
            if not o:
                continue

            direction = '+'
            if o[0] in ops:
                direction = o[0]
                o = o[1:]
            elif o[-1] in ops:
                direction = o[-1]
                o = o[:-1]

            orders.append((o, direction))

        return orders
