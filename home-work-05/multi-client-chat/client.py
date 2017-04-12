import socket
import logging
import threading
import json

logging.basicConfig(level=logging.INFO, format='%(name)s: %(message)s', )

HOST = "localhost"
PORT = 9000
READ_BUFFER = 1024
END_MARKER = "<end>"


def receive_package(data):
    return json.loads(data, encoding="utf8")


def send(client, name):
    while True:
        msg = input("\r\n " + name + " > ")
        client.send(send_package(name, msg))


def receive(client, name):
    while True:
        data = receive_end(client)
        pack = receive_package(data)
        print("\r\n" + pack["name"] + " > " + pack["message"])


def send_package(name, message):
    start_private_message = message.find("user:")
    if start_private_message > -1:
        to = message[start_private_message + 5:message.find(" ")]
        msg = message[start_private_message + 5 + len(to):]
    else:
        to = "All"
        msg = message

    pack = json.dumps({"name": name, "message": msg, "to": to})
    return bytes(pack + END_MARKER, encoding="utf8")


def receive_end(the_socket):
    total_data = []
    while True:
        data = str(the_socket.recv(READ_BUFFER), encoding="utf8")
        if END_MARKER in data:
            total_data.append(data[:data.find(END_MARKER)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            last_pair = total_data[-2] + total_data[-1]
            if END_MARKER in last_pair:
                total_data[-2] = last_pair[:last_pair.find(END_MARKER)]
                total_data.pop()
                break
    return ''.join(total_data)


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    logging.info("Connected to remote host...")

    user_name = input("Enter your name to enter the chat:")
    t = send_package(user_name, "")
    client.send(t)

    thread_send = threading.Thread(target=send, args=(client, user_name))
    thread_send.start()

    thread_receive = threading.Thread(target=receive, args=(client, user_name))
    thread_receive.start()
