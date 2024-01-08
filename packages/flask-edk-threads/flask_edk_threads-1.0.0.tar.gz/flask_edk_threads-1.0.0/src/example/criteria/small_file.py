from flask_edk_threads.abstract_criteria import AbstractCriteria


class SmallFile(AbstractCriteria):
    def true(self, criteria_desc):
        return criteria_desc.get("file_size") <= 1024 * 100
