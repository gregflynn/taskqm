from .task_service import TaskService
from .settings import Settings


class Board(object):
    def __init__(self, name, query):
        self.name = name
        self.query = query

    def render(self):
        tasks = TaskService.get_tasks(query=self.query)
        for task in tasks:
            for col in Settings.COLUMNS:
                print(task.get(col), end=' ')
            print()

    def render_status(self):
        pass
