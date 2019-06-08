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
    ColumnConfig('priority', display_name='\uf527'),
    ColumnConfig(
        'urgency',
        display_name='score', justify=ColumnConfig.RIGHT, fmt='{:.1f}'),
    ColumnConfig('tags')
]
CURRENT_COLUMNS = (
    COLUMNS[:2]
    + [ColumnConfig('description_annotate', display_name='description')]
    + COLUMNS[3:]
)
DONE_COLUMNS = [ColumnConfig('uuid', display_name='#')] + COLUMNS[1:]


class Settings(object):
    THEME_COLOR = Color.ORANGE
    PROJECT_COLOR = Color.PURPLE
    FILTERS_COLOR = Color.RED

    ANNOTATION_DATE_COLOR = Color.ORANGE
    ANNOTATION_INDENT = 2
    ANNOTATION_DATE_FORMAT = '%m/%d'

    PROMPT = ''
    TRUE = '\uf62b'
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
        },
        'description_annotate': {
            None: Color.YELLOW
        }
    }
