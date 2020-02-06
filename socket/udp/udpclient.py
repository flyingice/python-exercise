import socket

server_ip = 'localhost'
server_port = 20000

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    query = input('Input lowercase sentence: ')
    client_socket.sendto(query.encode(), (server_ip, server_port))
    response, server_address = client_socket.recvfrom(2048)
    print(response.decode())
    client_socket.close()
