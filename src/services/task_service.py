import json
from subprocess import check_output, run

from .task import Task


class TaskService(object):
    CMD = 'task'

    @classmethod
    def get_udas(cls):
        return cls._get_from_task('_uda')

    @classmethod
    def get_task_ids(cls):
        return cls._get_from_task('_ids')

    @classmethod
    def get_projects(cls):
        return cls._get_from_task('_projects')

    @classmethod
    def _get_from_task(cls, subtask):
        return sorted(set([
            x.strip().decode('utf-8')
            for x in check_output([cls.CMD, subtask]).split()
        ]))

    @classmethod
    def get_tasks(cls, query=None):
        cmd = [cls.CMD]
        if query:
            cmd.append(query)
        cmd.append('export')
        tasks = json.loads(check_output(cmd))
        return [Task(t) for t in tasks]

    @classmethod
    def edit(cls, taskid):
        run([cls.CMD, taskid, 'edit'])

    @classmethod
    def start(cls, taskid):
        run([cls.CMD, taskid, 'start'])

    @classmethod
    def stop(cls, taskid):
        run([cls.CMD, taskid, 'stop'])

    @classmethod
    def done(cls, taskid):
        run([cls.CMD, taskid, 'done'])

    @classmethod
    def annotate(cls, taskid, annotation):
        run([cls.CMD, taskid, 'annotate', annotation])

    @classmethod
    def view(cls, taskid):
        return check_output([cls.CMD, taskid]).decode('utf-8')
