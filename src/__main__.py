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

    PROJECTS = set(TaskService.get_projects())

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
        self.filter = None
        self._cmd_output = None

        self._board_switches = {}
        self._board_map = {}
        self._board_names = []
        self.board = None

        for board_config in Settings.BOARDS:
            name = board_config.name
            self._board_names.append(name)
            self._board_switches[name[0]] = name
            self._board_switches[name] = name
            self._board_map[name] = Board(
                name,
                board_config.query,
                board_config.columns,
                board_config.order
            )
            if board_config.default:
                self.board = name

        self.board = self.board or self._board_names[0]
        if self.current_board.count() == 0:
            self.board = self._board_names[0]

        self._status = StatusLine(self._board_names)
        self.precmd('')
        self.postcmd(False, '')

    @property
    def current_board(self):
        return self._board_map[self.board]

    #
    # Global
    #
    def do_project(self, arg):
        """select the project to filter on
        """
        self.project = arg if arg else None

    def complete_project(self, text, line, begidx, endidx):
        return sorted([
            name for name in self.PROJECTS if name.startswith(text)
        ])

    def do_filter(self, arg):
        """filter the tasks that are shown on boards
        """
        self.filter = arg if arg else None

    #
    # Board
    #
    def do_board(self, arg):
        """select the board to view
        """
        if arg not in self._board_map:
            arg = self._board_names[0]
        self.board = arg

    def complete_board(self, text, line, begidx, endidx):
        return sorted([
            name for name in self._board_names if name.startswith(text)
        ])

    def do_order(self, arg):
        """set the board task ordering
        """
        self.current_board.set_order(arg)

    def complete_order(self, text, line, begidx, endidx):
        matches = []

        for c in self.current_board.columns:
            col = c.display_name
            if not col:
                continue
            if col.startswith(text):
                matches.append(col)

        return matches

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

    def do_sync(self, arg):
        """sync tasks to the server
        """
        self.output(TaskService.sync())

    def do_task(self, arg):
        """talk to task directly
        """
        self.output(TaskService.task(arg))

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

        if self.filter:
            filters += self.filter

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
            print(self._status.render(
                self.board, self.current_board.order, self.project, self.filter
            ))
            self.current_board.render(self.get_filters())
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

        board_name = self._board_switches.get(line)
        if board_name:
            self.board = board_name


if __name__ == '__main__':
    TaskService.sync()
    try:
        TaskQM().cmdloop()
    except KeyboardInterrupt:
        pass
    TaskService.sync()
