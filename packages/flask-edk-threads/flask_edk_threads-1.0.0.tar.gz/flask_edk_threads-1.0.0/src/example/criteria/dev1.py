from flask_edk_threads.abstract_criteria import AbstractCriteria


class Dev1(AbstractCriteria):
    def true(self, criteria_desc):
        return criteria_desc.get("host") == "dev1"