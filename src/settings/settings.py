import os

from src.util import Color
from .column_config import ColumnConfig


USER_SETTINGS_PATH = f'{os.getenv("HOME")}/.taskqmrc'
SYSTEM_SETTINGS_PATH = '/etc/taskqmrc'


class Settings(object):
    THEME_COLOR = Color.ORANGE
    PROJECT_COLOR = Color.PURPLE
    FILTERS_COLOR = Color.RED
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
    CELL_COLORS = {
        'type': {
            'FTR': Color.GREEN,
            'IMP': Color.PURPLE,
            'BUG': (Color.WHITE, Color.RED)
        },
        'description_count': {
            None: Color.YELLOW
        }
    }
