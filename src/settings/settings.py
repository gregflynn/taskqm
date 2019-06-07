import os

from src.util import Color
from .column_config import ColumnConfig
from .board_config import BoardConfig


USER_SETTINGS_PATH = f'{os.getenv("HOME")}/.taskqmrc'
SYSTEM_SETTINGS_PATH = '/etc/taskqmrc'
COLUMNS = [
    ColumnConfig('id', display_name='#', justify=ColumnConfig.RIGHT),
    ColumnConfig('project'),
    ColumnConfig('description_count', display_name='description'),
    ColumnConfig('type'),
    ColumnConfig('size'),
    ColumnConfig('priority', display_name='p'),
    ColumnConfig(
        'urgency',
        display_name='score', justify=ColumnConfig.RIGHT, fmt='{:.1f}'),
    ColumnConfig('tags')
]
CURRENT_COLUMNS = COLUMNS[:2] + [ColumnConfig('description')] + COLUMNS[3:]
DONE_COLUMNS = [ColumnConfig('uuid', display_name='#')] + COLUMNS[1:]


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
        BoardConfig(
            'ready', '+PENDING -ACTIVE', COLUMNS, order='project,score-'
        ),
        BoardConfig(
            'current', '+ACTIVE', CURRENT_COLUMNS,
            default=True, order='project,start-'
        ),
        BoardConfig('done', '+COMPLETED', DONE_COLUMNS, order='end-')
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
