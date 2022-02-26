# library -> python socket communication
import socket


# public function:
#   input: none
#   return: IP adress of server, similar to type in terminal: hostname -I
# Note: function use socker library for get server ip adress, which is further used for
# get automatic acces in roslib.js to rosbridge_server(bridge between server - client)
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]

    except Exception:
        IP = "127.0.0.1"

    finally:
        s.close()

    return IP
