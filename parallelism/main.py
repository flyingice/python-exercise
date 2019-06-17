import common
import master
import workerNum

if __name__ == '__main__':
    master = master.Master()
    master.register_worker(workerNum.WorkerNum)
    intermeidate_result = master.map_task(common.map_function)
    master.reduce_task(common.reduce_function, intermeidate_result)
