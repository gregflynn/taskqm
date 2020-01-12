from collections import defaultdict


class TaskWarriorSettings:
    def __init__(self, taskrc_path):
        self._raw_data = {}
        self._uda_keys = defaultdict(list)
        self._parse_file(taskrc_path)
        self.udas = [
            UserDefinedAttribute(self, name, keys)
            for name, keys in self._uda_keys.items()
        ]

    def _parse_file(self, path):
        with open(path, 'r') as f:
            for line in f.readlines():
                line = line.strip()

                if line.startswith('include'):
                    path = line[8:]
                    self._parse_file(path)

                if '=' in line:
                    self._parse_setting(line)

    def _parse_setting(self, line):
        split_line = line.split('=', maxsplit=1)
        key_str, value = split_line

        # convert value lists
        if ',' in value:
            value = value.split(',')

        # save the raw key/value
        self._raw_data[key_str] = value

        # organize UDAs
        if key_str.startswith('uda'):
            _, uda_name, _ = key_str.split('.', maxsplit=2)
            self._uda_keys[uda_name].append(key_str)

    def get(self, key):
        return self._raw_data.get(key)


class UserDefinedAttribute:
    def __init__(self, taskrc, name, keys):
        self.name = name
        self.default = ''
        self.label = ''
        self.values = []

        for key in keys:
            value = taskrc.get(key)
            attr = key.split('.')[-1]
            setattr(self, attr, value)
