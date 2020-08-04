import master
import sys

# TODO: filesystem error management

# To customized the behavior, the user is supposed to provide
# the definitions of the following functions in mapreduce.py:
# def split_task(task)
# def map_function(content)
# def reduce_function(key, values)

if __name__ == "__main__":
    master = master.Master(task=sys.argv[1:])
    master.map_task()
    master.reduce_task()

    sys.exit(0)
