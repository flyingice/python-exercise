import logging
import multiprocessing


class Policy(object):
    def get_logging_level(self):
        return logging.DEBUG

    def get_parallelism_degree(self):
        return multiprocessing.cpu_count()
