import socket
import ssl
import configparser
import base64
import logging
import sys
import re

BUF_SIZE = 2048
PORT = 465  # SMTPS, use port 25 for SMTP
RECIPIENT = 'rainforest.vista@gmail.com'
MSG = ("To: {}\r\n"
       "Subject: This is the title\r\n"
       "\r\n"
       "This is the 1st line.\r\n"
       "This is the 2nd line.\r\n"
       "This is the last line.\r\n").format(RECIPIENT)


class SmtpClient:
    def __init__(self, sock):
        self.sock = sock

    def command(self, *args, buf_size=BUF_SIZE, status=None):
        if args:
            cmd = args[0] + '\r\n'
            logging.debug(cmd.encode())
            self.sock.send(cmd.encode())

        reply = self.sock.recv(buf_size)
        logging.debug(reply)
        if status and reply.decode()[:3] != str(status):
            logging.error('unexpected reply from the server')
            return False

        return True

    def smtp_handshaking(self, host):
        self.command(status=220)
        self.command('HELO {}'.format(host), status=250)

    def smtp_auth(self, user, passwd):
        self.command('AUTH LOGIN', status=334)
        self.command(base64.b64encode(user.encode()).decode(), status=334)
        if not self.command(base64.b64encode(passwd.encode()).decode(), status=235):
            logging.error('check credentials')
            sys.exit()

    def smtp_prep(self, sender):
        # MAIL FROM
        self.command('MAIL FROM: <{}>'.format(sender), status=250)
        # RCPT TO (multiple RCPT TO commands in case of multiple recipients)
        self.command('RCPT TO: <{}>'.format(RECIPIENT), status=250)

    def smtp_send(self):
        # DATA
        self.command('DATA', status=354)
        if not self.command('{}\r\n.'.format(MSG), status=250):
            logging.error('failed to send the message')

    def smtp_quit(self):
        self.command('QUIT', status=221)


def parse_config(filename):
    config = configparser.ConfigParser()
    with open(filename) as infile:
        config.read_file(infile)
    return config['DEFAULT']['sender'], config['DEFAULT']['passwd']


def validate_email(email):
    return re.match(r'^[\w.-]+@[\w.-]+$', email)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)

    try:
        sender, passwd = parse_config('./user.conf')
    except (OSError, KeyError, configparser.MissingSectionHeaderError) as err:
        logging.error(err)
        sys.exit()

    if not validate_email(sender):
        logging.error('invalid sender mail address')
        sys.exit()

    user, domain = sender.split('@', 1)[0], sender.split('@', 1)[1]
    host = 'smtp.' + domain

    logging.info('connecting to {0}:{1}...'.format(host, PORT))
    context = ssl.create_default_context()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            ssock.connect((host, PORT))
            logging.info(
                "connection established with {0}".format(ssock.version()))

            smtp_client = SmtpClient(ssock)
            smtp_client.smtp_handshaking(host)
            smtp_client.smtp_auth(user, passwd)
            smtp_client.smtp_prep(sender)
            smtp_client.smtp_send()
            smtp_client.smtp_quit()
