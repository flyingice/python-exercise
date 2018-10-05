#!/usr/bin/python

import os
import paramiko
import socket
import smtplib
from email.message import EmailMessage

hostname = 'ssh.freeshells.org'
username = 'flyingice'
command = 'date'


def remote_exec(hostname, username, command):
    try:
        client = paramiko.SSHClient()
        # load ~/.ssh/known_host by default
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # public key is required to be deployed first on the target host via ssh-copy-id
        client.connect(hostname=hostname, username=username)
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

    if 'res' in locals():
        return res


def main():
    res = remote_exec(hostname, username, command)
    if res:
        print(''.join(res))


if __name__ == '__main__':
    main()
