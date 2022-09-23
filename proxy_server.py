import socket
from threading import Thread


def serve(host, port):
    '''
    Starts the proxy server and spawns threads to handle client's requests concurrently
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)

        # accept connections from clients
        while True:
            client_socket, addr = server_socket.accept()
            print("Accepting connection from: ", addr)
            thread = Thread(target=handle_request, args=([client_socket]))
            thread.start()


def handle_request(client_socket):
    '''
    Handles forwarding requests to and from google on behalf of clients.
    '''
    with client_socket:
        while True:
            incoming_data = client_socket.recv(1024)
            if not incoming_data:
                break
            print("Forwarding Request to google")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as google_socket:
                google_socket.connect(("www.google.com", 80))
                google_socket.send(incoming_data)
                res = google_socket.recv(4096)
                print("Forwarding Response to client")
                client_socket.sendall(res)  # send response back to client


if __name__ == "__main__":
    serve("127.0.0.1", 8080)
