import socket
import logging
import threading
import json

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s', )

HOST = "localhost"
PORT = 9000
USER_AMOUNT = 10
READ_BUFFER = 1024
END_MARKER = "<end>"
CONNECTION_LIST = []


def send_package(name, message):
    pack = json.dumps({"name": name, "message": message})
    return bytes(pack + END_MARKER, encoding="utf8")


def type_message_decider(json_data):
    if not "to" in json_data:
        json_data["to"] = "All"
    return json_data


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
    return json.loads(''.join(total_data), encoding="utf8")


def client_thread(user_name, conn):
    while True:
        pack = type_message_decider(receive_end(conn))
        logging.debug("From %s to %s message: %s", pack["name"], pack["to"], pack["message"])
        b_usr(conn, pack)


def b_usr(conn, msg):
    for i in range(len(CONNECTION_LIST)):
        if CONNECTION_LIST[i][1] != conn:
            if msg["to"] == "All":
                CONNECTION_LIST[i][1].send(send_package(msg["name"], msg["message"]))
            else:
                if CONNECTION_LIST[i][0] == msg["to"]:
                    CONNECTION_LIST[i][1].send(send_package(msg["name"], msg["message"]))


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(USER_AMOUNT)

    logging.info("Waiting for connections on %s:%s" % (HOST, PORT))

    while True:
        conn, address = server.accept()
        pack = receive_end(conn)
        CONNECTION_LIST.append((pack["name"], conn))

        logging.info('Client %s connected with %s : %s', pack["name"], address[0], address[1])

        thread_client = threading.Thread(target=client_thread, args=(pack["name"], conn))
        thread_client.start()
