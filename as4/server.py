import socket
import threading

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"Received: {request.decode()}")
    client_socket.send("ACK".encode())
    client_socket.close()

    def main():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 9999))
        server.listen(5)
        print("Listening on port 9999")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

            if __name__ == "__main__":
                main()