from flask_edk_threads.abstract_event import AbstractEvent


class NothingEvent(AbstractEvent):
    def action(self): ...
