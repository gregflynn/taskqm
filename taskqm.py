from cmd import Cmd
from subprocess import run

from painter import TextColor, Painter


class TaskQM(Cmd):
    intro = 'Task Quartermaster'
    prompt = Painter.color(TextColor.BLUE, 'tqm> ')

    def __init__(self):
        super().__init__()
        self.project = None

    def do_list(self, arg):
        q = 'list'
        if arg:
            q += ' ' + arg
        self.run(q)

    def do_ls(self, arg):
        self.do_list(arg)

    def do_project(self, arg):
        if arg:
            self.project = arg
        else:
            self.project = None

    def do_exit(self, arg):
        return True

    def default(self, arg):
        if arg == 'EOF':
            return True
        self.run(arg)

    def run(self, prompt):
        print()
        if self.project:
            prompt += f' project:{self.project}'
        run(['task', *prompt.split(' ')])
        print()
        if self.project:
            print(Painter.color(TextColor.RED, f'project:{self.project}'))


if __name__ == '__main__':
    TaskQM().cmdloop()
