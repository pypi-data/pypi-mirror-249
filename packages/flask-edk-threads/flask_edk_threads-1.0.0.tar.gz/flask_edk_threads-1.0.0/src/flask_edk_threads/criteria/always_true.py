from flask_edk_threads.abstract_criteria import AbstractCriteria


class AlwaysTrue(AbstractCriteria):
    def true(self, criteria_desc):
        return True
