import socket

server_port = 20000

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    while True:
        connection_socket, client_address = server_socket.accept()
        data = connection_socket.recv(2048)
        # print the data and return as it is
        print("from {0} received: {1}".format(client_address, data.decode()))
        connection_socket.send(data)
        connection_socket.close()
