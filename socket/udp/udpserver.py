import socket

server_port = 20000

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', server_port))
    print("The server is ready to receive.")
    while True:
        query, clientAddress = server_socket.recvfrom(2048)
        response = query.decode().upper()
        server_socket.sendto(response.encode(), clientAddress)
