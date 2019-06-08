from subprocess import CalledProcessError, check_output

from src.settings import Settings, ColumnConfig
from src.services import TaskService
from .column import ColumnGroup


COLUMNS = Settings.SELECTOR_COLUMNS
if COLUMNS[0].name != 'id':
    COLUMNS = [ColumnConfig('id')] + Settings.SELECTOR_COLUMNS


class Selector(object):
    @classmethod
    def select(cls, query=None, project=None):
        tasks = ColumnGroup(
            cls._get_tasks(query, project), COLUMNS).render(header=False)

        try:
            line = check_output(
                f'echo "{tasks}" | fzf --ansi', shell=True).decode('utf-8')
            return line.split()[0]
        except CalledProcessError:
            return None

    @classmethod
    def _get_tasks(cls, query=None, project=None):
        tasks = []

        for task in TaskService.get_tasks(query=query):
            task_project = task.get('project') or ''
            if project is None or task_project.startswith(project):
                tasks.append(task)

        return tasks
