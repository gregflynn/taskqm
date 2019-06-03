import json
from subprocess import check_output

from .task import Task


class TaskService(object):
    @classmethod
    def get_udas(cls):
        return cls._get_from_task('_uda')

    @classmethod
    def get_task_ids(cls):
        return cls._get_from_task('_ids')

    @classmethod
    def get_projects(cls):
        return cls._get_from_task('_projects')

    @staticmethod
    def _get_from_task(subtask):
        return sorted(set([
            x.strip().decode('utf-8')
            for x in check_output(['task', subtask]).split()
        ]))

    @classmethod
    def get_tasks(cls, query=None):
        cmd = ['task']
        if query:
            cmd.append(query)
        cmd.append('export')
        tasks = json.loads(check_output(cmd))
        return [Task(t) for t in tasks]
