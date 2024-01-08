import importlib
import threading
from queue import Queue

from flask_edk_threads.abstract_event import AbstractEvent
from flask_edk_threads.criteria.always_true import AlwaysTrue
from flask_edk_threads.common import class_parser
import logging

from flask_edk_threads.events.nothing_event import NothingEvent

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("FTErrorLog.txt")
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class TaskThread(threading.Thread):
    def __init__(self, thread_name, criteria):
        super().__init__()
        self._thread_name = thread_name
        self.stop_event = threading.Event()
        self._events = Queue()
        if criteria is not None:
            clazz_info = class_parser(criteria)
            module = importlib.import_module(clazz_info.get("package"))
            clazz = getattr(module, clazz_info.get("class"))
            self._criteria = clazz()
        else:
            self._criteria = AlwaysTrue()

    @property
    def thread_name(self):
        return self._thread_name

    def qsize(self):
        return self._events.qsize()

    def run(self):
        while not self.stop_event.is_set():
            event = self._events.get()
            try:
                event.action()
                event.call_back()
            except Exception as e:
                event.fall_back()
                logger.error(e)

    def put(self, event: AbstractEvent):
        # if self.criteria(criteria_desc=event.criteria_desc()):
        #     print(self.thread_name, event.event_id, event.criteria_desc().get("host"),
        #           event.criteria_desc().get("file_size"))
            event.task_thread = self
            self._events.put(event)

    def get(self):
        self._events.get()

    def criteria(self, criteria_desc):
        return self._criteria.true(criteria_desc)

    def stop_thread(self):
        self.stop_event.set()
        self._events.put(NothingEvent())
