import os

from src.util import Color
from .column_config import ColumnConfig
from .board_config import BoardConfig


USER_SETTINGS_PATH = f'{os.getenv("HOME")}/.taskqmrc'
SYSTEM_SETTINGS_PATH = '/etc/taskqmrc'
COLUMNS = [
    ColumnConfig('id', display_name='#', justify=ColumnConfig.RIGHT),
    ColumnConfig(
        ('blocked', 'priority', 'type'),
        display_name='', justify=ColumnConfig.RIGHT),
    ColumnConfig('size', display_name='siz'),
    ColumnConfig(
        'urgency',
        display_name='score', justify=ColumnConfig.RIGHT, fmt='{:.1f}'),
    ColumnConfig('project'),
    ColumnConfig('description_smart', display_name='description'),
    ColumnConfig('tags')
]


class Settings(object):
    DEFAULT_PROJECT = 'home'
    THEME_COLOR = Color.ORANGE
    PROJECT_COLOR = Color.PURPLE
    FILTERS_COLOR = Color.RED

    ANNOTATION_DATE_COLOR = Color.ORANGE
    ANNOTATION_INDENT = 2
    ANNOTATION_DATE_FORMAT = '%m/%d'

    PROMPT = ''
    TRUE = '\uf62b'
    FALSE = ''
    PADDING = 2

    SELECTOR_COLUMNS = COLUMNS
    BOARDS = [
        BoardConfig(
            'blocked', '+BLOCKED', COLUMNS, order='project,score-'
        ),
        BoardConfig(
            'pending', '-ACTIVE +PENDING -BLOCKED', COLUMNS,
            order='project,score-'
        ),
        BoardConfig('active', '+ACTIVE', COLUMNS, default=True),
        BoardConfig('done', '+COMPLETED', COLUMNS, order='end-')
    ]
    CELL_COLORS = {
        'active': {
            True: Color.GREEN
        },
        'type': {
            'FTR': Color.GREEN,
            'IMP': Color.PURPLE,
            'BUG': Color.ORANGE,
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
            True: ''
        },
        'blocked': {
            True: '\uf655'
        },
        'type': {
            'BUG': '\ue009',
            'FTR': '\uf067',
            'IMP': '\uf0fe',
            'RES': 'R',
            'TSK': ''
        },
        'size': {
            'XS': '',
            'S': '█',
            'M': '██',
            'L': '███',
            'XL': '███'
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
