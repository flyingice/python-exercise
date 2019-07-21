import logging
import mapreduce
import multiprocessing as mp
import os
import os.path
import policydefault
import workerdefault


class Master(object):
    def __init__(self, task, policy=policydefault.PolicyDefault()):
        self.__task = task
        self.__policy = policy

        self.prepare()

    def prepare(self):
        # root logger settings
        logging.getLogger().setLevel(self.__policy.get_logging_level())
        # setup working dir
        if not os.path.exists(self.__policy.get_working_dir()):
            os.makedirs(self.__policy.get_working_dir())
        os.chdir(self.__policy.get_working_dir())
        # split the task
        self.__tasks = mapreduce.split_task(self.__task)

    def register_worker(self, worker):
        self.__worker = worker

    def map_task(self):
        if not 'worker' in self.__dict__:
            self.__worker = workerdefault.WorkerDefault

        try:
            with mp.Pool(processes=self.__policy.get_parallelism_degree()) as pool:
                pool.map(self.__worker(), self.__tasks)

        except OSError as err:
            logging.error(err)
        except mp.ProcessError as err:
            logging.error(err)
        finally:
            pool.close()

    def reduce_task(self):
        return mapreduce.do_reduce(len(self.__tasks))

    def cleanup(self):
        pass
