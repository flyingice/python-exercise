import worker


class WorkerNum(worker.Worker):
    def __init__(self):
        super().__init__()

    def __call__(self, args):
        super().__call__(args)
        return args ** 2
