
from pathlib import Path

from flask_edk_threads.abstract_event import AbstractEvent


class DBEvent(AbstractEvent):
    def __init__(self, host, file_size):
        super().__init__()
        self._host = host
        self._file_size = file_size

    def action(self):
        with open(Path("/flask_edk_threads\\src\\example\\output").joinpath(self.event_id), 'w') as f:
        # with open(Path("output").joinpath(self.event_id), 'w') as f:
            f.write(f'{self.task_thread.thread_name} {self.event_id} {self._host} {self._file_size}')

    def criteria_desc(self):
        return dict(host=self._host, file_size=self._file_size)
