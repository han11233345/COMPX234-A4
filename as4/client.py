import socket
import time


def send_and_receive(client, message, timeout=2):
    client.send(message.encode())
    client.settimeout(timeout)
    try:
        response = client.recv(4096).decode()
        return response
    except socket.timeout:
        return None

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    filename = "example.txt"
    response = None
    while response is None:
        response = send_and_receive(client, f"DOWNLOAD {filename}")

    if response.startswith("OK"):
        _, file_size = response.split()
        file_size = int(file_size)

        with open(f"downloaded_{filename}", "wb") as f:
            received_size = 0
            while received_size < file_size:
                data = client.recv(1024)
                f.write(data)
                received_size += len(data)

        print(f"Downloaded {filename}")
    else:
        print(response)


if __name__ == "__main__":
    main()