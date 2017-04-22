import socket
from packet import parse_packet, Packet
from utils import checksum, readFile
import time, struct


class BaseTransfer:
    """
    The base class for a transferer
    """
    def __init__(self, local=None, remote=None):
        self.local = local
        self.remote = remote

        self.setup()

    def setup(self):
        try:
            self.localSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if self.local is not None:
                self.localSocket.bind(self.local)
                print("Successfully setup socket at {} {}".format(self.local))
        except socket.error:
            import sys
            print("Cannot setup the socket.", file=sys.stderr)
            sys.exit(-1)

    def teardown(self):
        try:
            self.localSocket.close()
        except:
            pass


class BasicUDPTransfer(BaseTransfer):
    """
    unreliable file transfer
    """
    def send(self, data, flag=0):
        p = Packet(0, data, flag=flag)
        self.localSocket.sendto(bytes(p), self.remote)

    def recv(self):
        self.localSocket.settimeout(5)
        while True:
            try:
                message, address = self.localSocket.recvfrom(1024)
                _, _, flag, data = parse_packet(message)
                yield data
                # last packet, don't wait for timeout
                if flag == 2:
                    break
            except socket.timeout:
                print('end')
                break

    def sendFile(self, filename):
        print("start to send file: " + filename)
        # pack timestamp and filename
        timestamp = struct.pack('>f', time.time())

        # remove prefix
        bfilename = filename.split('/')[-1].encode('utf8')

        # send metadata
        self.send(timestamp + bfilename)
        for data in readFile(filename, chunk_size=Packet.DATA_LENGTH):
            self.send(data)

        # end flag
        self.send(bytes(), 2)

    def recvFile(self):
        print("waiting for file")

        # unpack metadata
        received = self.recv()

        data = next(received)
        start_time = struct.unpack('>f', data[:4])[0]
        filename = data[4:].decode('utf8')

        # start collect file chunks
        with open(filename, 'wb') as dl:
            for data in received:
                dl.write(data)
        print("{} transferred in {:.2f}ms".format(filename, (time.time() - start_time)))


class RDTTransfer(BaseTransfer):
    pass
