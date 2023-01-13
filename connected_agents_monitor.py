"""
connected_agents_monitor.py - maintains a list of active agents in the swarm.
"""

import socket
import threading
import datetime
import json


SERVER_BIND_IP = "127.0.0.1"


class ConnectedAgentsMonitor:
    def __init__(self, heartbeat_interface_port, agents_list_port):
        self.active_agents = {}

        self.heartbeat_thread = threading.Thread(target=self.run_server,
                                                 args=(heartbeat_interface_port, self.handle_incoming_heartbeat,))
        self.heartbeat_thread.start()

        self.agents_list_thread = threading.Thread(target=self.run_server,
                                                 args=(agents_list_port, self.handle_request_for_agents,))
        self.agents_list_thread.start()


    def run_server(self, bind_port, incoming_data_handler):
        broker_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        broker_server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        broker_server.bind((SERVER_BIND_IP, bind_port))
        broker_server.listen()
        conn, addr = broker_server.accept()

        while True:
            data = conn.recv(2 ** 16)  # TODO - put in a layer similar to TCP where we join our packets together?
            response = incoming_data_handler(data, addr)

            if response:
                conn.send(response)

            conn.close()
            conn, addr = broker_server.accept()


    def handle_incoming_heartbeat(self, msg_str, addr):
        incoming_heartbeat = json.loads(msg_str)
        agent_id = incoming_heartbeat["id"]
        timestamp = datetime.datetime.now()
        self.active_agents[agent_id] = {"timestamp": timestamp, "ip": addr[0]}


    def handle_request_for_agents(self, msg_str, addr):
        now = datetime.datetime.now()

        active_agents = []
        old_active_agents = list(self.active_agents.keys())
        for agent_id in old_active_agents:
            agent_data = self.active_agents[agent_id]
            last_timestamp_time = agent_data["timestamp"]
            agent_ip = agent_data["ip"]
            if now - last_timestamp_time < datetime.timedelta(seconds=10):
                active_agents.append((agent_ip, agent_id))
            else:
                del self.active_agents[agent_id]

        json_string = json.dumps(active_agents)
        return bytes(json_string, "utf-8")


if __name__ == "__main__":
    c = ConnectedAgentsMonitor(12000, 12001)
