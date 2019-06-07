import os

from src.util import Color
from .column_config import ColumnConfig
from .board_config import BoardConfig


USER_SETTINGS_PATH = f'{os.getenv("HOME")}/.taskqmrc'
SYSTEM_SETTINGS_PATH = '/etc/taskqmrc'
COLUMNS = [
    ColumnConfig('id', display_name='#', justify=ColumnConfig.RIGHT),
    ColumnConfig('type'),
    ColumnConfig('size'),
    ColumnConfig('project'),
    ColumnConfig('tags'),
    ColumnConfig('description_count', display_name='description'),
    ColumnConfig(
        'urgency',
        display_name='score', justify=ColumnConfig.RIGHT, fmt='{:.1f}')
]
CURRENT_COLUMNS = COLUMNS[:5] + [ColumnConfig('description')] + COLUMNS[6:]


class Settings(object):
    THEME_COLOR = Color.ORANGE
    PROJECT_COLOR = Color.PURPLE
    FILTERS_COLOR = Color.RED
    PROMPT = '>'
    TRUE = ''
    FALSE = ''
    PADDING = 2
    SELECTOR_COLUMNS = COLUMNS
    BOARDS = [
        BoardConfig('ready', '+PENDING -ACTIVE', COLUMNS),
        BoardConfig('curnt', '+ACTIVE', CURRENT_COLUMNS, default=True),
        BoardConfig('done', '+COMPLETED', COLUMNS)
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
