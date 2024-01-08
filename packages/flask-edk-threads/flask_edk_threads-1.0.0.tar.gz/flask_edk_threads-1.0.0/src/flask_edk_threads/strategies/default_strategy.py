from flask_edk_threads.abstract_event import AbstractEvent
from flask_edk_threads.strategies.abstract_strategy import AbstractStrategy


class DefaultStrategy(AbstractStrategy):

    def balance(self, event: AbstractEvent) -> int:
        length = self.task_thread_group.thread_count()
        # 策略1. 优先使用空闲的线程, 处理任务
        for i in range(length):
            if self.task_thread_group.index(i).qsize() == 0: return i

        # 策略2. 找出任务数最先的线程，并且剩余任务数 < 2. 即将空闲的线程， 处理任务
        min_index = self.min()
        if self.task_thread_group.index(min_index).qsize() <= 2: return i

        # 没有满足策略的线程，任务按条件进入对应的线程
        return -1

    def min(self) -> int:
        min_index = 0
        for i in range(1, self.task_thread_group.thread_count()):
            if self.task_thread_group.index(i - 1).qsize() < self.task_thread_group.index(i).qsize():
                min_index = i
        return min_index
