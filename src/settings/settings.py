import os


USER_SETTINGS_PATH = f'{os.getenv("HOME")}/.taskqmrc'
SYSTEM_SETTINGS_PATH = '/etc/taskqmrc'


class ColumnConfig(object):
    LEFT = 'l'
    RIGHT = 'r'

    def __init__(self, name, display_name=None, justify=None, fmt=None):
        if not display_name:
            display_name = name

        self.name = name
        self.display_name = display_name
        self.justify = justify or self.LEFT
        self.fmt = fmt or '{}'


class Settings(object):
    PROMPT = '>'
    TRUE = ''
    FALSE = ''
    PADDING = 2
    COLUMNS = [
        ColumnConfig('id', display_name='#', justify=ColumnConfig.RIGHT),
        ColumnConfig('is_active', display_name='A'),
        ColumnConfig('type'),
        ColumnConfig('size'),
        ColumnConfig('project'),
        ColumnConfig('tags'),
        ColumnConfig('description_count', display_name='description'),
        ColumnConfig(
            'urgency',
            display_name='score', justify=ColumnConfig.RIGHT, fmt='{:.1f}')
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
