from flask_edk_threads.abstract_criteria import AbstractCriteria


class MediumFile(AbstractCriteria):
    def true(self, criteria_desc):
        return 1024 * 100 < criteria_desc.get("file_size") <= 1024 * 800
