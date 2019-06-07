from src.settings import Settings
from src.util import Color


class StatusLine(object):
    ALL_PROJECTS = 'all'
    ACTIVE_BOARD_FG = Settings.THEME_COLOR
    ACTIVE_BOARD_BG = Color.BLACK
    INACTIVE_BOARD_FG = Color.WHITE
    INACTIVE_BOARD_BG = Color.BLACK

    def __init__(self, board_names):
        self._board_names = board_names

    def render(self, board, order, project):
        div = Divider(Settings.THEME_COLOR)
        line = ['\n']

        sections = []
        for board_section in self._board_sections(board):
            sections.extend([board_section, div])
        sections.pop()
        sections.append(self._order_section(order))

        line.append(self._render_sections(sections))
        line.append('  ')
        line.append(self._render_sections([self._project_section(project)]))

        return ''.join(line + ['\n'])

    def _render_sections(self, sections):
        line = []
        for idx, section in enumerate(sections):
            line.append(section.render(idx, sections))
        return ''.join(line)

    def _board_sections(self, board):
        def active(b):
            return b == board
        return [
            Section(
                b,
                self.ACTIVE_BOARD_FG if active(b) else self.INACTIVE_BOARD_FG,
                self.ACTIVE_BOARD_BG if active(b) else self.INACTIVE_BOARD_BG
            )
            for b in self._board_names
        ]

    def _project_section(self, project):
        project_name = project or self.ALL_PROJECTS
        return Section(f'{project_name}', Color.BLACK, Settings.PROJECT_COLOR)

    def _order_section(self, order):
        return Section(f'{order}', Color.BLACK, Settings.THEME_COLOR)


class Section(object):
    FIRST_ARROW = '\uE0BA'
    ARROW = '\uE0BC'

    def __init__(self, text, fg, bg):
        self.text = text
        self.fg = fg
        self.bg = bg

    def render(self, idx, sections):
        pre = ''
        text = self._render_text()

        next_section = self._next_section_color(idx, sections)
        if next_section:
            arrow = Color.paint(self.bg, next_section, self.ARROW)
        else:
            arrow = Color.paint(self.bg, self.ARROW)

        if idx == 0:
            pre = Color.paint(self.bg, self.FIRST_ARROW)

        return f'{pre}{Color.paint(self.fg, self.bg, text)}{arrow}'

    def _render_text(self):
        return f' {self.text} ' if self.text else self.text

    def _next_section_color(self, idx, sections):
        return sections[idx + 1].bg if len(sections) > idx + 1 else None


class Divider(Section):
    def __init__(self, color):
        super().__init__('', Color.WHITE, color)
