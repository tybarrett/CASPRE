"""ArtifactDistributionMaintainer.py - maintains a data structure that describes where each Artifact is hosted."""

import socket
import json
import ischedule

HOST = "127.0.0.1"
GET_AGENTS_PORT = "12001"


class ArtifactDistributionMaintainer:

    def __init__(self):
        self.host_id_to_artifacts = {}
        self.host_id_to_ip = {}

        ischedule.schedule(self.request_connected_agents, interval=1.0)
        ischedule.run_loop()


    def request_connected_agents(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, GET_AGENTS_PORT))
        sock.send(b"{}")

        response = sock.recv(1024)

        response_obj = json.loads(response.decode("utf-8"))
        for ip_str, id in response_obj:
            if id not in self.host_id_to_artifacts:
                self.host_id_to_artifacts[id] = []
                self.host_id_to_ip = ip_str
            # TODO - handle case where the IP changes (but maintains the same id)
            # TODO - is it possible for an agent to be maintaining artifacts when we first connect?
            #      - maybe build a request for that?


    def calculate_resiliency_level(self):
        # TODO - calculate resiliency level - how many agents we can lose without losing data (worst case)
        pass


    def calculate_stability(self):
        # TODO - calculate stability metric - describes (generally) how dependent artifacts are on other artifacts
        pass


    def calculate_urgency(self):
        # TODO calculate urgency metric - describes how close we are to losing data
        pass

