import os


USER_SETTINGS_PATH = f'{os.getenv("HOME")}/.taskqmrc'
SYSTEM_SETTINGS_PATH = '/etc/taskqmrc'


class Settings(object):
    PROMPT = '>'
    PADDING = 2
    COLUMNS = [
        {
            'name': 'id',
            'display_name': '#',
            'justified': 'r'
        }, {
            'name': 'is_active',
            'display_name': 'A'
        },
        {'name': 'type'},
        {'name': 'size'},
        {'name': 'project'},
        {'name': 'tags'},
        {
            'name': 'description_count',
            'display_name': ''
        }, {
            'name': 'urgency',
            'display_name': 'score',
            'justified': 'r',
            'format': '{:.1f}'
        }
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
