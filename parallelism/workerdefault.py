import logging
import mapreduce
import os


class WorkerDefault(object):
    def __init__(self):
        super().__init__()

    def __call__(self, task):
        logging.info("pid={0}, task={1}".format(os.getpid(), task))
        mapreduce.do_map(task)
