class Color(object):
    BLACK = '30'
    RED = '31'
    GREEN = '32'
    YELLOW = '33'
    BLUE = '34'
    PURPLE = '35'
    CYAN = '36'
    WHITE = '37'

    @staticmethod
    def fg(color):
        return '3' + str(int(color) % 10)

    @staticmethod
    def bg(color):
        return '4' + str(int(color) % 10)


class Painter(object):
    @staticmethod
    def color(fgcolor, arg2, arg3=None):
        """Return a colored string that can be printed

        Args:
            fgcolor (Color): the foreground color to apply to the text
            arg2 (Color|str): the background color or the text to color
            arg3 (str): the text to color if specifying a background color

        Returns:
            str: the colored string
        """
        fg = Color.fg(fgcolor)
        if arg3 is not None:
            return f'\033[{fg};{Color.bg(arg2)}m{arg3}\033[0m'
        return f'\033[{fg}m{arg2}\033[0m'
