from subprocess import CalledProcessError, check_output

from src.settings import Settings, ColumnConfig
from src.services import TaskService
from .column import Column


class Selector(object):
    @classmethod
    def select(cls, query=None, project=None):
        columns = Column.build_column_group(
            [
                t for t in TaskService.get_tasks(query=query)
                if project is None
                or (t.get('project') or '').startswith(project)
            ],
            columns=[ColumnConfig('id')] + Settings.COLUMNS
        )

        tasks = Column.column_group_content(columns)

        try:
            line = check_output(
                f'echo "{tasks}" | fzf', shell=True).decode('utf-8')
            return cls._get_task_line_id(line)
        except CalledProcessError:
            return None

    @classmethod
    def _get_task_line_id(cls, line):
        return line.split()[0]