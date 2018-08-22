import os.path
import easygui as gui


def write_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)


filename = gui.fileopenbox(default='~/Dev/cpp/leetcode/*.cpp')
if filename is None:
    exit(0)

with open(filename, 'r') as f:
    title = os.path.basename(filename)
    text = f.read()
    text_new = gui.textbox('Contents of {0}'.format(title), title, text, True)
    if text_new is None:
        exit(0)

    if text_new != text:  # user has modified the text
        label1 = 'Save as...'
        label2 = 'Overwrite'
        label3 = 'Cancel'
        choice = gui.buttonbox(
            'The file has been modified. Please choose: ', 'Warning', (label1, label2, label3))
        if choice == label1:
            save_to = gui.filesavebox()
            if save_to is None:
                exit(0)
            write_to_file(save_to, text_new)
        elif choice == label2:
            write_to_file(filename, text_new)
        else:
            pass
