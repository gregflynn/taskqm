from .painter import Painter, Color


class StatusLine(object):
    ALL_PROJECTS = 'all'
    ACTIVE_BOARD_FG = Color.BLACK
    ACTIVE_BOARD_BG = Color.GREEN
    INACTIVE_BOARD_FG = Color.WHITE
    INACTIVE_BOARD_BG = Color.BLACK

    def __init__(self, taskqm):
        self._taskqm = taskqm

    def render(self):
        sections = []
        sections.extend(self._board_sections())
        sections.extend([Divider(Color.YELLOW)])
        sections.extend(self._project_sections())

        line = '\n'

        for idx, section in enumerate(sections):
            line += section.render(idx, sections)

        return line

    def _board_sections(self):
        def active(b):
            return b == self._taskqm.board
        return [
            Section(
                b,
                self.ACTIVE_BOARD_FG if active(b) else self.INACTIVE_BOARD_FG,
                self.ACTIVE_BOARD_BG if active(b) else self.INACTIVE_BOARD_BG
            )
            for b in self._taskqm.BOARD_NAMES
        ]

    def _project_sections(self):
        project_name = self.ALL_PROJECTS
        if self._taskqm.project:
            project_name = self._taskqm.project
        return [Section(f'{project_name}', Color.BLACK, Color.PURPLE)]


class Section(object):
    ARROW = ''

    def __init__(self, text, fg, bg):
        self.text = text
        self.fg = fg
        self.bg = bg

    def render(self, idx, sections):
        pre = ''
        text = f' {self.text} ' if self.text else self.text
        arrow = ''

        next_section = self._next_section_color(idx, sections)
        if next_section:
            arrow = Painter.color(self.bg, next_section, self.ARROW)
        else:
            arrow = Painter.color(self.bg, self.ARROW)

        if idx == 0:
            pre = Painter.color(Color.BLACK, self.bg, self.ARROW)

        return f'{pre}{Painter.color(self.fg, self.bg, text)}{arrow}'

    def _next_section_color(self, idx, sections):
        return sections[idx + 1].bg if len(sections) > idx + 1 else None


class Divider(Section):
    def __init__(self, color):
        super().__init__('', Color.WHITE, color)
