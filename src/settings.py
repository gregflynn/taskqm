import os


USER_SETTINGS_PATH = f'{os.getenv("HOME")}/.taskqmrc'
SYSTEM_SETTINGS_PATH = '/etc/taskqmrc'


class Settings(object):
    PROMPT = '>'
    PADDING = 2
    COLUMNS = [
        ('id', '#', 'r'),
        ('is_active', ''),
        'type',
        'size',
        'project',
        'tags',
        ('description_count', ''),
        ('urgency', 'score', 'r', '{:.1f}')
    ]
    BOARDS = [
        {
            'name': 'ready',
            'query': '+PENDING'
        }, {
            'name': 'in progress',
            'query': '+ACTIVE'
        }, {
            'name': 'done',
            'query': '+COMPLETED'
        }
    ]
