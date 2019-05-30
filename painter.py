class TextColor(object):
    BLACK = '30'
    RED = '31'
    GREEN = '32'
    YELLOW = '33'
    BLUE = '34'
    PURPLE = '35'
    CYAN = '36'
    WHITE = '37'


class Painter(object):
    @staticmethod
    def color(color, text):
        return '\033[{}m{}\033[0m'.format(color, text)
