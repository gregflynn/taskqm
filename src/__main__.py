from cmd import Cmd
from subprocess import run

from src.services import TaskService
from src.settings import Settings
from src.ui import Board, StatusLine, Selector, TaskQMStdOut
from src.util import Color


class TaskQM(Cmd):
    intro = ''
    prompt = Color.paint(Settings.THEME_COLOR, Settings.PROMPT + ' ')
    doc_header = Color.paint(Settings.THEME_COLOR, 'Commands:')
    ruler = ''

    PROJECTS = set(TaskService.get_projects())
    DEFAULT_BURNDOWN = 'daily'
    BURNDOWN_PERIODS = {'daily', 'weekly', 'monthly'}

    def __init__(self):
        super().__init__(stdout=TaskQMStdOut())
        self.project = None
        self.filter = None
        self._cmd_output = None

        self._board_switches = {}
        self._board_map = {}
        self._board_names = []
        self.board = None

        for idx, board_config in enumerate(Settings.BOARDS):
            name = board_config.name
            self._board_names.append(name)
            self._board_switches[str(idx + 1)] = name
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
        board_idx = self._board_names.index(self.board)

        while self.current_board.count() == 0 and board_idx > 0:
            board_idx -= 1
            self.board = self._board_names[board_idx]

        self._status = StatusLine(self._board_names, self._board_map)

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
            try:
                idx = int(arg) - 1
                arg = self._board_names[idx]
            except (ValueError, IndexError):
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
        self.fallback_select(
            'View Task',
            lambda tid: self.output(TaskService.view(tid)),
            arg=arg
        )

    def do_edit(self, arg):
        """edit the given task
        """
        self.fallback_select(
            'Edit Task', lambda tid: TaskService.edit(tid), arg=arg
        )

    def do_start(self, arg):
        """start the given task
        """
        self.fallback_select(
            'Start Task',
            lambda tid: TaskService.start(tid),
            arg=arg,
            query='+PENDING -ACTIVE'
        )

    def do_stop(self, arg):
        """stop the given task
        """
        self.fallback_select(
            'Stop Task',
            lambda tid: TaskService.stop(tid),
            arg=arg,
            query='+ACTIVE'
        )

    def do_done(self, arg):
        """finish the given task
        """
        self.fallback_select(
            'Finish Task',
            lambda tid: TaskService.done(tid),
            arg=arg,
            query='+ACTIVE'
        )

    def do_annotate(self, arg):
        """annotate the given task
        """
        def set_annotation(tid):
            annotation = self.input('annotation')
            if annotation:
                TaskService.annotate(tid, annotation)

        # use the current board's query if there are tasks on it
        query = None
        if self.current_board.count() > 0:
            query = self.current_board.query

        self.fallback_select(
            'Annotate Task', set_annotation, arg=arg, query=query
        )

    def do_add(self, arg):
        """add a task
        """
        description = arg if arg else self.input('description')
        if not description:
            self.output('description required')
            return

        project = self.input(
            'project', default=self.project or Settings.DEFAULT_PROJECT)

        udas = {}

        for uda in TaskService.get_udas():
            default = Settings.UDA_DEFAULTS.get(uda)
            example = Settings.UDA_INPUTS.get(uda)
            uda_value = self.input(uda, default=default, examples=example)
            if uda_value not in {'', None}:
                udas[uda] = uda_value

        tags_input = self.input('tags') or ''
        tags = tags_input.split(' ')
        tags = tags if tags != [''] else None

        output = TaskService.add(
            description, project=project, tags=tags, udas=udas)
        if output:
            self.output(output)

    def do_depend(self, arg):
        """mark a task dependent on another
        """
        def select_parent(tid):
            def set_depends(parent_tid):
                TaskService.depends(tid, parent_tid)

            self.fallback_select('Precursor Task', set_depends, query='+PENDING')

        self.fallback_select('Dependent Task', select_parent, query='+PENDING')

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
    def fallback_select(self, header, action, arg=None, query=None):
        if not arg:
            arg = Selector.select(
                query=query, project=self.project, header=header
            )

        if arg:
            action(arg)

    def get_filters(self):
        filters = []

        if self.project:
            filters.append(f'project:{self.project}')

        if self.filter:
            filters.append(f'/{self.filter}/')

        return ' '.join(filters)

    def input(self, text, default=None, examples=None):
        examples_str = f' ({examples})' if examples else ''
        default_str = f' [{default}]' if default else ''
        t = f'{text}{examples_str}{default_str}: '
        return input(Color.paint(Settings.THEME_COLOR, t)) or default

    def output(self, text):
        if self._cmd_output is None:
            self._cmd_output = text
        else:
            self._cmd_output += '\n' + text

    #
    # Overrides
    #
    def precmd(self, line):
        if line == 'EOF':
            raise QuitException
        return line

    def postcmd(self, stop, line):
        run(['clear'])
        print(self._status.render(
            self.board, self.current_board.order, self.project, self.filter
        ))
        self.current_board.render(self.get_filters())

        if self._cmd_output:
            print('\n' + self._cmd_output)
            self._cmd_output = None
        else:
            self.do_help(None)
        self.stdout.dump()

        return stop

    def emptyline(self):
        """no-op so the default behavior of execing last command doesn't happen
        """

    def default(self, line):
        board_name = self._board_switches.get(line)
        if board_name:
            self.board = board_name


class QuitException(Exception):
    pass


if __name__ == '__main__':
    TaskService.sync()
    taskqm = TaskQM()

    while True:
        try:
            taskqm.postcmd(None, None)
            taskqm.cmdloop()
        except QuitException:
            break
        except KeyboardInterrupt:
            pass

    TaskService.sync()
