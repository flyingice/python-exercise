#!/usr/bin/python

import os
import os.path
import paramiko
import socket

hostname = 'ec2-15-188-69-16.eu-west-3.compute.amazonaws.com'
username = 'ec2-user'
keyfile = '~/.ssh/EC2-default.key'
command = 'date'


def remote_exec(hostname, username, command):
    try:
        client = paramiko.SSHClient()
        # load ~/.ssh/known_host by default
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # public key is required to be deployed first on the target host via ssh-copy-id
        # keyfile is ~/.ssh/id_rsa by default
        client.connect(hostname=hostname, username=username,
                       key_filename=os.path.expanduser(keyfile))
        (stdin, stdout, stderr) = client.exec_command(command)

        res = list()
        for line in stdout:
            res.append(line)
    except (IOError, socket.error,
            paramiko.ssh_exception.BadHostKeyException,
            paramiko.ssh_exception.AuthenticationException,
            paramiko.ssh_exception.SSHException) as error:
        print(error)
    finally:
        client.close()

    return res if 'res' in locals() else ''


def main():
    res = remote_exec(hostname, username, command)
    if res:
        print(''.join(res), end='')


if __name__ == '__main__':
    main()
