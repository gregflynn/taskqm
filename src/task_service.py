import json
from subprocess import check_output

from .task import Task


class TaskService(object):
    @classmethod
    def get_udas(cls):
        udas = set(check_output(['task', '_udas']).split())
        return sorted(udas)

    @classmethod
    def get_task_ids(cls):
        ids = check_output(['task', '_ids']).split()
        return ids

    @classmethod
    def get_projects(cls):
        projects = check_output(['task', '_projects']).split()
        return sorted(set(projects))

    @classmethod
    def get_tasks(cls, query=None):
        cmd = ['task']
        if query:
            cmd.append(query)
        cmd.append('export')
        print(cmd)
        tasks = json.loads(check_output(cmd))
        return [Task(t) for t in tasks]
