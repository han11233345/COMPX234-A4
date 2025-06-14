import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))
    filename = "example.txt"
    client.send(f"DOWNLOAD {filename}".encode())

    response = client.recv(4096).decode()
    print(response)

    if __name__ == "__main__":
        main()