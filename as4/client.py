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

def download_file(client, filename):
    response = None
    while response is None:
        response = send_and_receive(client, f"DOWNLOAD {filename}")

    if response.startswith("OK"):
        _, file_size = response.split()
        file_size = int(file_size)

        with open(f"downloaded_{filename}", "wb") as f:
            received_size = 0
            while received_size < file_size:
                try:
                    client.settimeout(2)
                    data = client.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    received_size += len(data)
                except socket.timeout:
                    print(f"Timeout while downloading {filename}, retrying...")
                    client.send(f"RESUME {filename} {received_size}".encode())
                    continue

        print(f"Downloaded {filename}")
    else:
        print(response)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))


    file_list = ["example1.txt", "example2.txt"]
    for filename in file_list:
        download_file(client, filename)


if __name__ == "__main__":
    main()