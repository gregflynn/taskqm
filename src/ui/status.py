from .color import Color


class StatusLine(object):
    ALL_PROJECTS = 'all'
    ACTIVE_BOARD_FG = Color.BLACK
    ACTIVE_BOARD_BG = Color.BLUE
    INACTIVE_BOARD_FG = Color.WHITE
    INACTIVE_BOARD_BG = Color.BLACK

    def __init__(self, taskqm):
        self._taskqm = taskqm

    def render(self):
        div = Divider(Color.YELLOW)
        sections = [div]
        for board_section in self._board_sections():
            sections.extend([board_section, div])
        sections.extend(self._project_sections())
        sections.extend(self._order_sections())

        line = '\n'

        for idx, section in enumerate(sections):
            line += section.render(idx, sections)

        return line

    def _board_sections(self):
        def active(b):
            return b == self._taskqm.board
        return [
            BoardSection(
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

    def _order_sections(self):
        return [Section(f'{self._taskqm.order}', Color.BLACK, Color.RED)]


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


class BoardSection(Section):
    def _render_text(self):
        return self.text


class Divider(Section):
    def __init__(self, color):
        super().__init__('', Color.WHITE, color)
