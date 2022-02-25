# library -> python socket communication
import socket

# library -> python interpret bytes as packed binary data
import struct

# library -> python codecs registry
from codecs import encode, decode

"""

Documentation for recieve data from server-client realtime interface:

https://www.universal-robots.com/articles/ur/remote-control-via-tcpip/

"""


class Robot_info(object):
    # public classmethod:
    #   input: none
    #   return none
    # Note: Init ip adress of robot with static ports for communication
    @classmethod
    def connect(cls, ip_adress):
        # ip address of host
        cls.HOST = ip_adress
        # Interface realtime = port number
        cls.PORT_RT = 30003
        cls.PORT_DS = 29999

    # public classmethod:
    #   input: none
    #   return none
    # Note: This method represents remote acces to play button in polyscope
    @classmethod
    def play_button(cls):
        HOST = cls.HOST
        PORT = cls.PORT_DS

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        post = encode("play" + "\n")
        s.send(post)

        s.close()

    @classmethod
    def test_connection(cls):
        HOST = cls.HOST
        PORT = cls.PORT_RT

        # setup python socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connectino server to client
        s.connect((HOST, PORT))

    # public classmethod:
    #   input: none
    #   return temperature of engines, current of engines
    # Note: This method create socket communication with robot and parse data,
    # which are post to route.
    @classmethod
    def get_data(cls):
        # it is neccesery to get new socket instance becouse
        # buffer heh
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connectino server to client
        s.connect((cls.HOST, cls.PORT_RT))

        # message size
        packet_1 = s.recv(4)
        # time
        packet_2 = s.recv(8)
        # q target
        packet_3 = s.recv(48)
        # qd target
        packet_4 = s.recv(48)
        # qdd target
        packet_5 = s.recv(48)
        # I target
        packet_6 = s.recv(48)
        # M target
        packet_7 = s.recv(48)
        # q actual
        packet_8 = s.recv(48)
        # qd actual
        packet_9 = s.recv(48)
        # I actual
        # packet_10 = s.recv(48)
        packet_10_1 = s.recv(8)
        packet_10_1 = encode(packet_10_1, "hex")
        packet_10_1 = decode(packet_10_1, "hex")
        curr_1 = struct.unpack("!d", packet_10_1)[0]
        # print("current1[A] = " + str(curr_1))

        packet_10_2 = s.recv(8)
        packet_10_2 = encode(packet_10_2, "hex")
        packet_10_2 = decode(packet_10_2, "hex")
        curr_2 = struct.unpack("!d", packet_10_2)[0]

        packet_10_3 = s.recv(8)
        packet_10_3 = encode(packet_10_3, "hex")
        packet_10_3 = decode(packet_10_3, "hex")
        curr_3 = struct.unpack("!d", packet_10_3)[0]
        # print("current3[A] = " + str(curr_3))

        packet_10_4 = s.recv(8)
        packet_10_4 = encode(packet_10_4, "hex")
        packet_10_4 = decode(packet_10_4, "hex")
        curr_4 = struct.unpack("!d", packet_10_4)[0]
        # print("current4[A] = " + str(curr_4))

        packet_10_5 = s.recv(8)
        packet_10_5 = encode(packet_10_5, "hex")
        packet_10_5 = decode(packet_10_5, "hex")
        curr_5 = struct.unpack("!d", packet_10_5)[0]
        # print("current5[A] = " + str(curr_5))

        packet_10_6 = s.recv(8)
        packet_10_6 = encode(packet_10_6, "hex")
        packet_10_6 = decode(packet_10_6, "hex")
        curr_6 = struct.unpack("!d", packet_10_6)[0]
        # print("current6[A] = " + str(curr_6))

        # I control
        packet_11 = s.recv(48)

        # Tool vector actual
        # -------X----------
        packet_12 = s.recv(8)
        packet_12 = encode(packet_12, "hex")
        packet_12 = decode(packet_12, "hex")
        x = struct.unpack("!d", packet_12)[0]
        # print("\nX = " + str(x*1000))

        # -------Y----------
        packet_13 = s.recv(8)
        packet_13 = encode(packet_13, "hex")
        packet_13 = decode(packet_13, "hex")
        y = struct.unpack("!d", packet_13)[0]
        # print("Y = " + str(y*1000))

        # -------Z----------
        packet_14 = s.recv(8)
        packet_14 = encode(packet_14, "hex")
        packet_14 = decode(packet_14, "hex")
        z = struct.unpack("!d", packet_14)[0]
        # print("Z = " + str(z*1000)+ "\n")

        # -------RX----------
        packet_15 = s.recv(8)
        # -------RY----------
        packet_16 = s.recv(8)
        # -------RZ----------
        packet_17 = s.recv(8)

        # tcp speed actual
        packet_18 = s.recv(48)
        # tcp force
        packet_19 = s.recv(48)
        # tool vector target
        packet_20 = s.recv(48)
        # tcp speed target
        packet_21 = s.recv(48)
        # digitals input bits
        packet_22 = s.recv(8)

        # Motor temperatures
        # base
        packet_23 = s.recv(8)
        packet_23 = encode(packet_23, "hex")
        packet_23 = decode(packet_23, "hex")
        temp1 = struct.unpack("!d", packet_23)[0]
        # print("Temp. base = " + str(temp1))

        # shoulder
        packet_24 = s.recv(8)
        packet_24 = encode(packet_24, "hex")
        packet_24 = decode(packet_24, "hex")
        temp2 = struct.unpack("!d", packet_24)[0]
        # print("Temp. shoulder = " + str(temp2))

        # elbow
        packet_25 = s.recv(8)
        packet_25 = encode(packet_25, "hex")
        packet_25 = decode(packet_25, "hex")
        temp3 = struct.unpack("!d", packet_25)[0]
        # print("Temp. elbow = " + str(temp3))

        # wrist1
        packet_26 = s.recv(8)
        packet_26 = encode(packet_26, "hex")
        packet_26 = decode(packet_26, "hex")
        temp4 = struct.unpack("!d", packet_26)[0]
        # print("Temp. wrist 1 = " + str(temp4))

        # wrist2
        packet_27 = s.recv(8)
        packet_27 = encode(packet_27, "hex")
        packet_27 = decode(packet_27, "hex")
        temp5 = struct.unpack("!d", packet_27)[0]
        # print("Temp. wrist 2 = " + str(temp5))

        # wrist3
        packet_28 = s.recv(8)
        packet_28 = encode(packet_28, "hex")
        packet_28 = decode(packet_28, "hex")
        temp6 = struct.unpack("!d", packet_28)[0]
        # print("Temp. wrist 3 = " + str(temp6) + "\n")

        return [
            curr_1,
            curr_2,
            curr_3,
            curr_4,
            curr_5,
            curr_6,
            temp1,
            temp2,
            temp3,
            temp4,
            temp5,
            temp6,
        ]

        s.close()
