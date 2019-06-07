from cmd import Cmd
from subprocess import run

from src.services import TaskService
from src.settings import Settings
from src.ui import Board, StatusLine, Selector
from src.util import Color


class TaskQM(Cmd):
    intro = ''
    prompt = Color.paint(Settings.THEME_COLOR, Settings.PROMPT + ' ')
    doc_header = Color.paint(Settings.THEME_COLOR, 'Commands: [help command]')
    ruler = ''

    BOARD_NAMES = ['pend', 'start', 'done']
    BOARDS = {
        'pend': Board('pend', '+PENDING -ACTIVE'),
        'start': Board('start', '+ACTIVE'),
        'done': Board('done', '+DONE')
    }
    DEFAULT_BOARD = 'start'
    BACKUP_BOARD = 'pend'
    PROJECTS = set(TaskService.get_projects())
    DEFAULT_ORDER = 'score-'

    DEFAULT_PROJECT = 'home'
    UDA_DEFAULTS = {
        'type': 'TSK'
    }

    DEFAULT_BURNDOWN = 'daily'
    BURNDOWN_PERIODS = {'daily', 'weekly', 'monthly'}

    # commands that don't alter the board, so we don't clear and reprint it
    NON_BOARD_COMMANDS = {'h', 'help', 'view'}

    def __init__(self):
        super().__init__()
        self.project = None
        self.order = self.DEFAULT_ORDER
        self._cmd_output = None

        if self.BOARDS[self.DEFAULT_BOARD].count():
            self.board = self.DEFAULT_BOARD
        else:
            self.board = self.BACKUP_BOARD

        self._status = StatusLine(self)
        self.precmd('')
        self.postcmd(False, '')

    #
    # Project
    #
    def do_project(self, arg):
        """select the project to filter on
        """
        self.project = arg if arg else None

    def complete_project(self, text, line, begidx, endidx):
        return sorted([
            name for name in self.PROJECTS if name.startswith(text)
        ])

    #
    # Ordering
    #
    def do_order(self, arg):
        """set the board task ordering
        """
        self.order = arg or self.DEFAULT_ORDER

    def complete_order(self, text, line, begidx, endidx):
        matches = []

        for c in Settings.COLUMNS:
            col = c.get('display_name') or c.get('name')
            if not col:
                continue
            if col.startswith(text):
                matches.append(col)

        return matches

    #
    # Board
    #
    def do_board(self, arg):
        """select the board to view
        """
        if arg not in self.BOARDS:
            print(f'Unknown board specified: {arg}')
            arg = self.DEFAULT_BOARD
        self.board = arg

    def complete_board(self, text, line, begidx, endidx):
        return sorted([
            name for name in self.BOARD_NAMES if name.startswith(text)
        ])

    def do_burndown(self, arg):
        """show a burndown graph
        """
        arg = arg or self.DEFAULT_BURNDOWN
        if arg not in self.BURNDOWN_PERIODS:
            self.output('Unknown Burndown Period')
            return
        TaskService.burndown(arg)

    def complete_burndown(self, text, line, begidx, endidx):
        return sorted([p for p in self.BURNDOWN_PERIODS if p.startswith(text)])

    def do_summary(self, arg):
        """show project summaries
        """
        TaskService.summary()

    #
    # Task Commands
    #
    def do_view(self, arg):
        """view details of a task
        """
        arg = self.fallback_select(arg, '-DONE')
        if arg:
            self._cmd_output = TaskService.view(arg)

    def do_edit(self, arg):
        """edit the given task
        """
        arg = self.fallback_select(arg, '-DONE')
        if arg:
            TaskService.edit(arg)

    def do_start(self, arg):
        """start the given task
        """
        arg = self.fallback_select(arg, '+PENDING -ACTIVE')
        if arg:
            TaskService.start(arg)

    def do_stop(self, arg):
        """stop the given task
        """
        arg = self.fallback_select(arg, '+ACTIVE')
        if arg:
            TaskService.stop(arg)

    def do_done(self, arg):
        """finish the given task
        """
        arg = self.fallback_select(arg, '+ACTIVE')
        if arg:
            TaskService.done(arg)

    def do_annotate(self, arg):
        """annotate the given task
        """
        arg = self.fallback_select(arg, '-DONE')
        if arg:
            annotation = self.input('annotation')
            if annotation:
                TaskService.annotate(arg, annotation)

    def do_add(self, arg):
        """add a task
        """
        description = arg if arg else self.input('description')
        if not description:
            self.output('description required')
            return

        project = self.input(
            'project', default=self.project or self.DEFAULT_PROJECT)

        udas = {}

        for uda in TaskService.get_udas():
            uda_value = self.input(uda, default=self.UDA_DEFAULTS.get(uda))
            if uda_value not in {'', None}:
                udas[uda] = uda_value

        tags_input = self.input('tags') or ''
        tags = tags_input.split(' ')
        tags = tags if tags != [''] else None

        output = TaskService.add(
            description, project=project, tags=tags, udas=udas)
        if output:
            self.output(output)

    def do_task(self, arg):
        """talk to task directly
        """
        self.output(TaskService.task(arg))

    #
    # Help
    #
    do_h = Cmd.do_help
    complete_h = Cmd.complete_help

    #
    # Helpers
    #
    def should_print_board(self, line):
        return (
            (not line or line.split()[0] not in self.NON_BOARD_COMMANDS)
            and not self._cmd_output
        )

    def fallback_select(self, arg, query):
        if arg:
            return arg

        return Selector.select(query, project=self.project)

    def get_filters(self):
        filters = ''

        if self.project:
            filters += f' project:{self.project}'

        return filters

    def input(self, text, default=None):
        if default:
            t = f'{text} [{default}]: '
        else:
            t = f'{text}: '
        return input(Color.paint(Settings.THEME_COLOR, t)) or default

    def output(self, text):
        self._cmd_output = text

    #
    # Overrides
    #
    def precmd(self, line):
        if line == 'EOF':
            raise KeyboardInterrupt
        return line

    def postcmd(self, stop, line):
        print_board = self.should_print_board(line)
        if print_board:
            run(['clear'])
            if line:
                print(f'{self.prompt}{line}')

        if self._cmd_output:
            print(self._cmd_output)
            self._cmd_output = None

        if print_board:
            print(self._status.render())
            self.BOARDS[self.board].render(self.get_filters(), self.order)
        return stop

    def emptyline(self):
        """no-op so the default behavior of execing last command doesn't happen
        """

    def default(self, line):
        try:
            if line in TaskService.get_task_ids():
                self.do_view(line)
                return
        except Exception:
            pass

        if line == 'q':
            self.board = self.BOARD_NAMES[0]
        elif line == 'w':
            self.board = self.BOARD_NAMES[1]
        elif line == 'e':
            self.board = self.BOARD_NAMES[2]

        print('default')


if __name__ == '__main__':
    try:
        TaskQM().cmdloop()
    except KeyboardInterrupt:
        pass
