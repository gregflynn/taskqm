from src.services import TaskService
from .column import ColumnGroup


class Board(object):
    def __init__(self, name, query, columns, order):
        self.name = name
        self.query = query
        self.columns = columns
        self.order = self._parse_order(order)
        self._col_map = {c.display_name: c.name for c in columns}
        self._default_order = self.order

    def count(self):
        return len(TaskService.get_tasks(query=self.query))

    def set_order(self, order):
        self.order = self._parse_order(order) if order else self._default_order

    def render(self, filters):
        tasks = self._get_sorted_tasks(filters)
        print(ColumnGroup(tasks, self.columns).render())

    def _get_sorted_tasks(self, filters):
        tasks = TaskService.get_tasks(query=f'{self.query} {filters}')

        for o, direction in reversed(self.order):
            key = self._col_map.get(o) or o
            reverse = direction == '-'
            tasks = sorted(
                tasks,
                # https://stackoverflow.com/a/18411610
                key=lambda t: (
                    t.get(key) is not None if reverse
                    else t.get(key) is None, t.get(key)),
                reverse=reverse
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
