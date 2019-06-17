import logging
import os


class Worker(object):
    def __init__(self):
        pass

    def __call__(self, args):
        logging.debug("pid={0}, args={1}".format(os.getpid(), args))
