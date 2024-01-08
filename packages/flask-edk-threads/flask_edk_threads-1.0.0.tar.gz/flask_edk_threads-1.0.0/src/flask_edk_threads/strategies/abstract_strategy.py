import abc

from flask_edk_threads.abstract_event import AbstractEvent
# from flask_threads.task_thread_group import TaskThreadGroup


class AbstractStrategy(abc.ABC):
    def __init__(self, task_thread_group):
        self.task_thread_group = task_thread_group

    def distribute(self, event: AbstractEvent):
        i = self.balance(event=event)
        self.criteria(i, event)

    def balance(self, event: AbstractEvent) -> int:
        return -1

    def criteria(self, i: int, event: AbstractEvent):
        if self.task_thread_group.criteria(event.criteria_desc()):
            if i == -1:
                for task_thread in self.task_thread_group.task_threads:
                    if task_thread.criteria(criteria_desc=event.criteria_desc()):
                        task_thread.put(event)
            else:
                self.task_thread_group.task_threads[i].put(event)
