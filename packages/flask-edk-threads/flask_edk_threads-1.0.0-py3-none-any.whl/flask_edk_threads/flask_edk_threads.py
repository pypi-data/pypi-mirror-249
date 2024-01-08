import logging
from pathlib import Path

from lxml import etree

from flask_edk_threads.common import name, criteria, strategy
from flask_edk_threads.task_thread import TaskThread
from flask_edk_threads.task_thread_group import TaskThreadGroup

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("FTErrorLog.txt")
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class FlaskEDKThreads(object):
    def __init__(self, app=None, config_file: Path = None):
        self._config_file = config_file
        self.thread_groups = []
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions['flask_threads'] = self
        self.load_config()
        self.start()

    def append(self, thread_group):
        self.thread_groups.append(thread_group)

    def load_config(self):
        element = etree.parse(self._config_file).getroot()
        for thread_group_element in element:
            if thread_group_element.tag == "ThreadGroup":
                thg = TaskThreadGroup(name(thread_group_element), criteria(thread_group_element),
                                      strategy(thread_group_element))
                for thread_element in thread_group_element:
                    thd = TaskThread(name(thread_element), criteria(thread_element))
                    thg.add(thd)
                self.append(thg)

    def start(self):
        for thread_group in self.thread_groups:
            thread_group.start()

    def put(self, event):
        for thread_group in self.thread_groups:
            thread_group.put(event)

    def stop_ft(self):
        for thread_group in self.thread_groups:
            thread_group.stop_thread_group()
