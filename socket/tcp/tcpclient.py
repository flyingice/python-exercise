import socket

server_address = "localhost"
server_port = 20000

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    query = input("please type a string: ")
    client_socket.send(query.encode())
    response = client_socket.recv(2048)
    client_socket.close()
    print(response.decode())
