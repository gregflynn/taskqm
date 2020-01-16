from datetime import datetime

from src.settings import Settings
from src.util import Color


class Task(object):
    DATE_PARSE_FMT = '%Y%m%dT%H%M%SZ'
    ANNOTATION_PAD = Settings.ANNOTATION_INDENT * ' '

    def __init__(self, data, task_map):
        self._data = data
        self._task_map = task_map

    @property
    def id(self):
        i = self._data.get('id')
        if i == 0:
            i = self.uuid
        return i

    @property
    def uuid(self):
        return self._data.get('uuid')

    @property
    def active(self):
        return len(self._data.get('start', '')) > 0

    @property
    def done(self):
        return len(self._data.get('end', '')) > 0

    @property
    def blocked(self):
        for uuid in self.dependency_uuids:
            dependency = self._task_map.get(uuid)

            if dependency and not dependency.done:
                return True

        return False

    @property
    def dependency_uuids(self):
        return (self._data.get('depends') or '').split(',')

    @property
    def description_smart(self):
        return (
            self.description_annotate if self.active
            else self.description_count
        )

    @property
    def description_count(self):
        description = self._data.get('description', 'none')
        num_annotations = len(self._data.get('annotations', []))
        if num_annotations:
            description += f' [{num_annotations}]'
        return description

    @property
    def description_annotate(self):
        description = self._data.get('description', 'none')
        annotations = [
            (
                datetime.strptime(a['entry'], self.DATE_PARSE_FMT).now(),
                a['description']
            )
            for a in self._data.get('annotations', [])
        ]

        annotation_lines = []
        for annotation in annotations:
            date_str = annotation[0].strftime(Settings.ANNOTATION_DATE_FORMAT)
            date_colored = Color.paint(
                Settings.ANNOTATION_DATE_COLOR, date_str
            )
            annotation_lines.append(
                f'{self.ANNOTATION_PAD}{date_colored}: {annotation[1]}'
            )

        return '\n'.join([description] + annotation_lines)

    def get(self, col):
        is_composite_col = isinstance(col, tuple)
        ret_data = []

        for c in col if is_composite_col else [col]:
            ret_data.append(
                getattr(self, c) if hasattr(self, c) else self._data.get(c)
            )

        return tuple(ret_data) if is_composite_col else ret_data[0]
