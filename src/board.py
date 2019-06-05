from .column import Column
from .task_service import TaskService
from .settings import Settings


class Board(object):
    def __init__(self, name, query):
        self.name = name
        self.query = query

    def count(self):
        return len(TaskService.get_tasks(query=self.query))

    def render(self, filters, order):
        columns = [Column(c) for c in Settings.COLUMNS]
        tasks = self._get_sorted_tasks(columns, filters, order)
        padding = Settings.PADDING * ' '

        for task in tasks:
            for col in columns:
                col.add(task)

        for col in columns:
            print(col.header(), end=padding)
        print()

        for col in columns:
            print(col.header_line(), end=padding)
        print()

        for idx in range(len(tasks)):
            for col in columns:
                print(col.render(idx), end=padding)
            print()

    def _get_sorted_tasks(self, columns, filters, order):
        col_map = {c.display_name: c.name for c in columns}
        tasks = TaskService.get_tasks(query=f'{self.query} {filters}')

        for o, directon in reversed(self._parse_order(order)):
            key = col_map.get(o) or o
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
