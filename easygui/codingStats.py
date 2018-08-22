import os
import os.path
import easygui as gui


def count_lines(filename):
    cnt = 0
    with open(filename) as f:
        for line in f:
            cnt += 1
    return cnt


def count_total_lines():
    cnt = 0
    for key in stats:
        cnt += stats[key][1]
    return cnt


def show_results():
    msg = []
    for key in stats:
        msg.append('{0} {1} file(s) containing {2} line(s) in total'.format(
            stats[key][0], key, stats[key][1]))
    return '\n'.join(msg)


stats = dict()  # file_type -> (file_count, line_count)
directory = gui.diropenbox(default='~/Dev')
if directory is None:
    exit(0)

for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        (root, ext) = os.path.splitext(filename)
        if ext in ('.cpp', '.py', '.sh'):
            stats.setdefault(ext, [0, 0])
            stats[ext][0] += 1
            stats[ext][1] += count_lines(os.path.join(dirpath, filename))

title = 'Statistics'
msg = 'You have written {0} line(s) of code'.format(count_total_lines())
result = gui.textbox(msg, title, show_results())
