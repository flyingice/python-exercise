import logging
import multiprocessing as mp
import policy
import worker


class Master(object):
    def __init__(self, policy=policy.Policy()):
        self.policy = policy

        # root logger settings
        logging.getLogger().setLevel(self.policy.get_logging_level())

    def register_worker(self, worker):
        self.worker = worker

    def prepare(self):
        pass

    def map_task(self, map_function, args=()):
        if not 'worker' in self.__dict__:
            self.worker = worker.Worker

        try:
            tasks = map_function(args)
            with mp.Pool(processes=self.policy.get_parallelism_degree()) as pool:
                res = pool.map(self.worker(), tasks)
        except mp.ProcessError as err:
            logging.error(err)
        finally:
            return res if 'res' in locals() else []

    def reduce_task(self, reduce_function, args=()):
        return reduce_function(args)

    def cleanup(self):
        pass
