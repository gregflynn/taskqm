from .column import Column
from .task_service import TaskService
from .settings import Settings


class Board(object):
    def __init__(self, name, query):
        self.name = name
        self.query = query

    def count(self):
        return len(TaskService.get_tasks(query=self.query))

    def render(self, filters):
        tasks = TaskService.get_tasks(query=f'{self.query} {filters}')
        padding = Settings.PADDING * ' '

        columns = [Column(c) for c in Settings.COLUMNS]
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
