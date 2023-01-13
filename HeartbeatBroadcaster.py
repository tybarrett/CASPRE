"""HeartbeatBroadcaster.py - Broadcasts our heartbeat message to the network periodically."""

import socket
import uuid
import json

import netifaces
import ischedule


BROADCAST_INTERFACE = ""
HEARTBEAT_DESTINATION_PORT = 12000


class HeartbeatBroadcaster:
    def __init__(self):
        self.host_id = uuid.getnode()

        # addresses = netifaces.ifaddresses(BROADCAST_INTERFACE)[netifaces.AF_INET]
        # self.broadcast_ip = addresses[0]["broadcast"]
        self.broadcast_ip = "127.0.0.1"
        print(self.broadcast_ip)

        # heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        # heartbeat_thread.start()


        ischedule.schedule(self.send_heartbeat, interval=1.0)
        ischedule.run_loop()


    def send_heartbeat(self):
        heartbeat_packet = {}
        heartbeat_packet["id"] = self.host_id
        heartbeat_packet_str = json.dumps(heartbeat_packet)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.broadcast_ip, HEARTBEAT_DESTINATION_PORT))
        sock.send(heartbeat_packet_str.encode("utf-8"))
        print(heartbeat_packet_str)


if __name__ == "__main__":
    hb = HeartbeatBroadcaster()
