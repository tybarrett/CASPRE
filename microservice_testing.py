import socket
import time

HOST = "127.0.0.1"
HEARTBEAT_PORT = 12000
GET_AGENTS_PORT = 12001


def test_active_agents():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, GET_AGENTS_PORT))
    sock.send(b"{}") # Has to contain actual data, not just an empty string.

    response = sock.recv(1024)

    return response.decode("utf-8")


def send_unit_heartbeat(agent_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, HEARTBEAT_PORT))
    json_string = "{\"id\": " + str(agent_id) + "}"
    sock.send(json_string.encode("utf-8"))  # Has to contain actual data, not just an empty string.

    response = sock.recv(1024)

    return response.decode("utf-8")


if __name__ == "__main__":
    print(test_active_agents())
    print(send_unit_heartbeat(1))
    print(test_active_agents())
    print(send_unit_heartbeat(2))
    print(test_active_agents())
    time.sleep(10)
    print(test_active_agents())

