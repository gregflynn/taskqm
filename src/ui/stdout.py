class TaskQMStdOut(object):
    def __init__(self):
        self._buffer = []

    def write(self, text):
        self._buffer.append(text)

    def flush(self):
        pass

    def dump(self):
        output = ''.join(self._buffer)
        if output:
            print(output)
        self._buffer = []
