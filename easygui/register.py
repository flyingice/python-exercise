import easygui as gui


def register():
    msg = 'Please fill in personal information'
    title = 'Account Management'
    field_name = ['*Alias', '*Real Name', 'Fix', '*Mobile', 'QQ', '*Email']
    field_value = gui.multenterbox(msg, title, field_name)

    while True:
        if field_value is None:
            exit(0)

        msg = []  # error msg
        for i, v in enumerate(field_name):
            if v.startswith('*') and not field_value[i].strip():
                msg.append('{0} is a required field.'.format(v[1:]))

        if not msg:
            for i, v in enumerate(field_name):
                msg.append("{0} : {1}".format(v, field_value[i]))
            gui.msgbox('\n'.join(msg), title)
            break
        else:
            field_value = gui.multenterbox('\n'.join(msg), title, field_name)


register()
