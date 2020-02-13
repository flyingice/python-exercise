import socket
import logging

server_port = 80

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)

    while True:
        connection_socket, client_address = server_socket.accept()

        http_request = connection_socket.recv(2048).decode()
        logging.debug("http request from {0}:\n{1}".format(
            client_address, http_request))

        filename = http_request.split('\r\n', 1)[0].split()[1]
        filename = 'index.html' if filename == '/' else filename
        logging.debug("target resource: {0}".format(filename))

        response = str()
        try:
            with open(filename, "r") as infile:
                content = infile.read()
                response = ("HTTP/1.1 200 OK\r\n"
                            "Content-Type: text/html\r\n"
                            "Content-Length: {0}\r\n"
                            "\r\n{1}").format(len(content), content)
        except OSError:
            logging.error("can not find {0}".format(filename))
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        connection_socket.send(response.encode())
        connection_socket.close()
