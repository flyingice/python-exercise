import logging
import multiprocessing
import os
import os.path


class PolicyDefault(object):
    """The customized policy should inherit from PolicyDefault and implements the following functions"""

    def get_logging_level(self):
        return logging.DEBUG

    def get_parallelism_degree(self):
        return multiprocessing.cpu_count()

    def get_working_dir(self):
        return os.path.join(os.getenv("TMPDIR"), "mapreduce")

    def get_auto_cleanup(self):
        return False
