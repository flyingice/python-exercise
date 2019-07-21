import master
import sys

if __name__ == '__main__':
    master = master.Master(task=sys.argv[1:])
    master.map_task()
    master.reduce_task()

    sys.exit(0)
