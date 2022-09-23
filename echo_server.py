import socket
from threading import Thread


def echo_server(host, port):
    '''
    Starts the echo server and spawns threads to handle client's requests concurrently
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)

        # accept connections from clients
        while True:
            client_socket, addr = server_socket.accept()
            print("Accepting connection from: ", addr)
            thread = Thread(target=handle_connection, args=([client_socket]))
            thread.start()


def handle_connection(client_socket):
    '''
    Handles reading data from, and echoing data back to the server.
    '''
    with client_socket:
        print(client_socket)
        while True:
            incoming_data = client_socket.recv(1024)
            if not incoming_data:
                break
            client_socket.sendall(incoming_data)


if __name__ == "__main__":
    echo_server("127.0.0.1", 8080)
