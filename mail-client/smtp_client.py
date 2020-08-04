import socket
import ssl
import configparser
import base64
import logging
import re

CRLF = "\r\n"
BUF_SIZE = 2048
PORT = 465  # SMTPS, use port 25 for SMTP


class SmtpClient:
    def __init__(self, sock):
        self.sock = sock

    def command(self, *args, buf_size=BUF_SIZE, status=None):
        if args:
            cmd = args[0] + CRLF
            logging.debug(cmd.encode())
            self.sock.send(cmd.encode())

        reply = self.sock.recv(buf_size)
        logging.debug(reply)
        if status and reply.decode()[:3] != str(status):
            logging.error("unexpected reply from the server")
            raise OSError

    def smtp_handshaking(self, host):
        self.command(status=220)
        self.command("HELO {}".format(host), status=250)

    def smtp_auth(self, user, passwd):
        self.command("AUTH LOGIN", status=334)
        self.command(base64.b64encode(user.encode()).decode(), status=334)
        self.command(base64.b64encode(passwd.encode()).decode(), status=235)

    def smtp_prep(self, sender, recipient):
        # MAIL FROM
        self.command("MAIL FROM: <{}>".format(sender), status=250)
        # RCPT TO (multiple RCPT TO commands in case of multiple recipients)
        for address in recipient:
            self.command("RCPT TO: <{}>".format(address), status=250)

    def smtp_send(self, data):
        # DATA
        self.command("DATA", status=354)
        self.command("{0}{1}.".format(data, CRLF), status=250)

    def smtp_quit(self):
        self.command("QUIT", status=221)


def parse_config(filename):
    config = configparser.ConfigParser()
    with open(filename) as infile:
        config.read_file(infile)
    sender, passwd = config["DEFAULT"]["sender"], config["DEFAULT"]["passwd"]
    validate_email(sender)
    return sender, passwd


def parse_data(filename):
    recipient = []
    lines = []
    with open(filename) as infile:
        # parse header subject, to etc..
        for line in infile:
            lines.append(line.strip())
            if lines[-1] == "":
                break
            key, value = lines[-1].split(":", maxsplit=1)
            if key.lower() == "to":
                recipient = [address.strip() for address in value.split(",")]

        for address in recipient:
            validate_email(address)

        lines.extend([line.strip() for line in infile.readlines()])

    return recipient, "{}".format(CRLF).join(lines)


def validate_email(email):
    if re.match(r"^[\w.-]+@[\w.-]+$", email) is None:
        raise ValueError


def get_user(sender):
    return sender.split("@", 1)[0]


def get_host(sender):
    return "smtp.{}".format(sender.split("@", 1)[1])


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    try:
        sender, passwd = parse_config("etc/user.conf")
        recipient, data = parse_data("etc/data.txt")

        host = get_host(sender)
        logging.info("connecting to {0}:{1}...".format(host, PORT))
        context = ssl.create_default_context()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.connect((host, PORT))
                logging.info("connection established with {0}".format(ssock.version()))

                smtp_client = SmtpClient(ssock)
                smtp_client.smtp_handshaking(host)
                smtp_client.smtp_auth(get_user(sender), passwd)
                smtp_client.smtp_prep(sender, recipient)
                smtp_client.smtp_send(data)
                smtp_client.smtp_quit()
    except ValueError as err:
        logging.error("invalid email address\r\n{}".format(err))
    except (KeyError, configparser.MissingSectionHeaderError) as err:
        logging.error("invalid config file\r\n{}".format(err))
    except OSError as err:
        logging.error("smtp failure\r\n{}".format(err))
