import socket
import time

HOST = 'localhost'
PORT = 12000
MAX_ATTEMPTS = 10
TIMEOUT = 1


def ping(address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)
    client_socket.sendto("ping".encode(), address)
    return client_socket.recv(2048)


if __name__ == "__main__":
    for i in range(MAX_ATTEMPTS):
        try:
            start_time = time.time()
            ping((HOST, PORT))
            end_time = time.time()
            print("seq={0} rtt={1}s".format(i, end_time - start_time))
        except socket.timeout:
            print("request timeout")
