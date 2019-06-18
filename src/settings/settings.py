import os

from src.util import Color
from .column_config import ColumnConfig
from .board_config import BoardConfig


USER_SETTINGS_PATH = f'{os.getenv("HOME")}/.taskqmrc'
SYSTEM_SETTINGS_PATH = '/etc/taskqmrc'
COLUMNS = [
    ColumnConfig('id', display_name='#', justify=ColumnConfig.RIGHT),
    ColumnConfig('active', display_name='A'),
    ColumnConfig('project'),
    ColumnConfig('description_smart', display_name='description'),
    ColumnConfig('blocked', display_name=''),
    ColumnConfig('priority', display_name=''),
    ColumnConfig('type', display_name=''),
    ColumnConfig('size'),
    ColumnConfig(
        'urgency',
        display_name='score', justify=ColumnConfig.RIGHT, fmt='{:.1f}'),
    ColumnConfig('tags')
]
DONE_COLUMNS = [ColumnConfig('uuid', display_name='#')] + COLUMNS[1:]


class Settings(object):
    DEFAULT_PROJECT = 'home'
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
            'ready', '+PENDING', COLUMNS, order='active-,project,score-'
        ),
        BoardConfig('done', '+COMPLETED', DONE_COLUMNS, order='end-')
    ]
    CELL_COLORS = {
        'active': {
            True: Color.GREEN
        },
        'type': {
            'FTR': Color.GREEN,
            'IMP': Color.PURPLE,
            'BUG': Color.RED,
            'RES': Color.BLUE
        },
        'size': {
            'XS': Color.GREEN,
            'S': Color.GREEN,
            'M': Color.YELLOW,
            'L': Color.ORANGE,
            'XL': Color.RED
        },
        'priority': {
            'H': Color.RED,
            'L': Color.BLUE
        },
        'description_count': {
            None: Color.YELLOW
        },
        'description_annotate': {
            None: Color.YELLOW
        },
        'description_smart': {
            None: Color.YELLOW
        },
        'blocked': {
            None: Color.RED
        }
    }
    CELL_REPLACEMENTS = {
        'active': {
            True: '\ue238'
        },
        'blocked': {
            True: ''
        },
        'type': {
            'BUG': '⚠',
            'FTR': '★',
            'IMP': '+',
            'RES': '🧪',
            'TSK': ''
        },
        'size': {
            'XS': '████',
            'S': '█',
            'M': '██',
            'L': '███',
            'XL': '████'
        },
        'priority': {
            'H': '\uf062',
            'M': '',
            'L': '\uf063'
        }
    }
    UDA_DEFAULTS = {
        'priority': 'M',
        'size': 'M',
        'type': 'TSK'
    }
    UDA_INPUTS = {
        'priority': 'H,M,L',
        'size': 'XS,S,M,L,XL',
        'type': 'BUG,TSK,FTR,IMP,RES'
    }
