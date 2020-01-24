from src.settings import Settings
from src.util import Color


class StatusLine(object):
    ALL_PROJECTS = 'all'
    ACTIVE_BOARD_FG = Settings.THEME_COLOR
    ACTIVE_BOARD_BG = Color.BLACK
    INACTIVE_BOARD_FG = Color.WHITE
    INACTIVE_BOARD_BG = Color.BLACK

    def __init__(self, board_names, board_map):
        self._board_names = board_names
        self._board_map = board_map

    def render(self, board, order, project, filters):
        spacer = '   '
        line = [
            '\n',
            self._board_sections(board),
            spacer,
            self._order_sections(order),
            spacer
        ]

        if project:
            line.append(self._project_sections(project))
            line.append(spacer)

        if filters:
            line.append(self._filter_sections(filters))

        return ''.join(line + ['\n'])

    @staticmethod
    def _render_sections(*sections):
        line = [
            section.render(i, sections) for i, section in enumerate(sections)
        ]
        return ''.join(line)

    def _board_sections(self, board):
        def active(b):
            return b == board
        label = Section('board', self.ACTIVE_BOARD_BG, self.ACTIVE_BOARD_FG)
        boards = [
            Section(
                f'{i + 1}:{b} ({self._board_map[b].count()})',
                self.ACTIVE_BOARD_FG if active(b) else self.INACTIVE_BOARD_FG,
                self.ACTIVE_BOARD_BG if active(b) else self.INACTIVE_BOARD_BG
            )
            for i, b in enumerate(self._board_names)
        ]
        return self._render_sections(label, *boards)

    def _project_sections(self, project):
        return self._render_sections(
            Section('project', Color.BLACK, Settings.PROJECT_COLOR),
            Section(project, Settings.PROJECT_COLOR, Color.BLACK)
        )

    def _order_sections(self, order):
        order = ','.join([f'{c}{d}' for c, d in order])
        return self._render_sections(
            Section('order', Color.BLACK, Settings.THEME_COLOR),
            Section(order, Settings.THEME_COLOR, Color.BLACK)
        )

    def _filter_sections(self, filters):
        f = filters.replace(' ', ',')
        return self._render_sections(
            Section('filter', Color.BLACK, Settings.FILTERS_COLOR),
            Section(f, Settings.FILTERS_COLOR, Color.BLACK)
        )


class Section(object):
    def __init__(self, text, fg, bg):
        self.text = text
        self.fg = fg
        self.bg = bg

    def render(self, idx, sections):
        lpad = ' '
        rpad = ' '

        if idx > 0:
            # assume idx 0 is the label
            rpad = ''

        return Color.paint(self.fg, self.bg, f'{lpad}{self.text}{rpad}')
