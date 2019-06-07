from subprocess import CalledProcessError, check_output

from src.settings import Settings, ColumnConfig
from src.services import TaskService
from .column import ColumnGroup


class Selector(object):
    @classmethod
    def select(cls, query=None, project=None):
        tasks = ColumnGroup(
            [
                t for t in TaskService.get_tasks(query=query)
                if project is None
                or (t.get('project') or '').startswith(project)
            ],
            [ColumnConfig('id')] + Settings.SELECTOR_COLUMNS
        ).render(header=False)

        try:
            line = check_output(
                f'echo "{tasks}" | fzf --ansi', shell=True).decode('utf-8')
            return cls._get_task_line_id(line)
        except CalledProcessError:
            return None

    @classmethod
    def _get_task_line_id(cls, line):
        return line.split()[0]
