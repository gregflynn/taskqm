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
        sections.extend(self._project_sections())

        line = '\n'

        for idx, section in enumerate(sections):
            line += section.render(
                sections[idx + 1] if len(sections) > idx + 1 else None
            )

        return line

    def _board_sections(self):
        return [
            Section(
                b,
                (
                    self.ACTIVE_BOARD_FG
                    if b == self._taskqm.board
                    else self.INACTIVE_BOARD_FG
                ), (
                    self.ACTIVE_BOARD_BG
                    if b == self._taskqm.board
                    else self.INACTIVE_BOARD_BG
                )
            )
            for b in self._taskqm.BOARD_NAMES
        ]

    def _project_sections(self):
        project_name = self.ALL_PROJECTS
        if self._taskqm.project:
            project_name = self._taskqm.project
        return [Section(f'project:{project_name}', Color.BLACK, Color.PURPLE)]


class Section(object):
    ARROW = ''

    def __init__(self, text, fg, bg):
        self.text = text
        self.fg = fg
        self.bg = bg

    def render(self, next_section=None):
        text = f' {self.text} '
        arrow = ''
        if next_section:
            arrow = Painter.color(self.bg, next_section.bg, self.ARROW)
        else:
            arrow = Painter.color(self.bg, self.ARROW)

        return f'{Painter.color(self.fg, self.bg, text)}{arrow}'
