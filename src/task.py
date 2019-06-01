class Task(object):
    def __init__(self, data):
        self._data = data

    @property
    def is_active(self):
        return 'start' in self._data and len(self._data['start']) > 0

    @property
    def description_count(self):
        description = self._data.get('description', 'none')
        num_annotations = len(self._data.get('annotations', []))
        if num_annotations:
            description += f' [{num_annotations}]'
        return description

    def get(self, col):
        if hasattr(self, col):
            return getattr(self, col)
        return self._data.get(col)
