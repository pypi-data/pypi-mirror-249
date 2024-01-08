from flask_edk_threads.abstract_event import AbstractEvent
from flask_edk_threads.criteria.always_true import AlwaysTrue
from flask_edk_threads.common import new_instance
from flask_edk_threads.strategies.only_criteria_strategy import OnlyCriteriaStrategy
from flask_edk_threads.task_thread import TaskThread


class TaskThreadGroup:
    def __init__(self, thread_group_name, criteria, strategy):
        self._thread_group_name = thread_group_name
        self.task_threads = []
        self._criteria = AlwaysTrue() if criteria is None else new_instance(criteria)
        self._strategy = OnlyCriteriaStrategy(self) if strategy is None else new_instance(strategy, task_thread_group=self)

    @property
    def thread_group_name(self):
        return self._thread_group_name

    def index(self, i) -> TaskThread:
        return self.task_threads[i]

    def thread_count(self):
        return len(self.task_threads)

    def criteria(self, criteria_desc):
        return self._criteria.true(criteria_desc)

    def put(self, event: AbstractEvent):
        self._strategy.distribute(event)
        # if self.criteria(event.criteria_desc()):
        #     for task in self.task_threads:
        #         task.put(event)

    # def distribute(self, event: AbstractEvent):
    #     ...

    def add(self, thread):
        self.task_threads.append(thread)

    def start(self):
        for thread in self.task_threads:
            thread.start()

    def stop_thread_group(self):
        for task_thread in self.task_threads:
            task_thread.stop_thread()
