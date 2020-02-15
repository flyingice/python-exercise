import socket
import threading
import logging

PORT = 55555
MAX_CONNECTION = 10
BUF_SIZE = 2048


class HttpProxy(threading.Thread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def run(self):
        try:
            request = self.sock.recv(BUF_SIZE)
            # forward the http request to the original server
            host = str()
            for line in request.decode().split('\r\n'):
                if line[:5].upper() == 'HOST:':
                    host = line.split()[1]

            if not host:
                logging.error("can not determine host")
                return

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
                server_sock.connect((host, 80))
                logging.debug(
                    "forwarding the http request to {0}:\r\n{1}".format(host, request))
                server_sock.send(request)

                reply = server_sock.recv(BUF_SIZE)
                logging.debug(
                    "forwarding the http reply to client:\r\n{}".format(reply))
                self.sock.send(reply)
        except OSError as err:
            logging.error(err)
        finally:
            self.sock.close()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("starting http proxy...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # prevent '[Errno 98] Address already in use' in case of too short delay between executions
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', PORT))
        sock.listen(MAX_CONNECTION)
        while True:
            conn_sock, _ = sock.accept()
            HttpProxy(conn_sock).start()
