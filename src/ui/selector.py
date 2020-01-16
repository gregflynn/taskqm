from subprocess import CalledProcessError, check_output

from src.settings import Settings, ColumnConfig
from src.services import TaskService
from .column import ColumnGroup


COLUMNS = Settings.SELECTOR_COLUMNS
if COLUMNS[0].name != 'id':
    COLUMNS = [ColumnConfig('id')] + Settings.SELECTOR_COLUMNS


class Selector(object):
    @classmethod
    def select(cls, query='+PENDING', project=None, header=''):
        try:
            column_group = ColumnGroup(cls._get_tasks(query, project), COLUMNS)
            line = cls._select_task(column_group, header)
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

    @classmethod
    def _select_task(cls, column_group, header):
        hlines = 2
        tasks = column_group.render()

        if header:
            tasks = f'{header}\n\n{tasks}'
            hlines = 4

        cmd = f'echo "{tasks}" | fzf --ansi --header-lines={hlines} --reverse --inline-info'  # noqa
        return check_output(cmd, shell=True).decode('utf8')
