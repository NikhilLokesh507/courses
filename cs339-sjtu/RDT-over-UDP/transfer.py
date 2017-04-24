import socket
from packet import parse_packet, make_packet, make_ack, DATA_LENGTH, MAX_SIZE, SEQ_MAX
from utils import checksum, readFile
import time, struct, sys
import random

from utils import timeit


class BaseTransfer:
    """
    The base class for a transferer, subclasses only need to
    implement send and recv method
    """
    def __init__(self, port=None, prob_loss=0.0):
        self.local = port
        self.prob_loss = prob_loss
        self.setup()

    def setup(self):
        try:
            self.localSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if self.local is not None:
                self.localSocket.bind(('', self.local))
                print("Successfully setup socket at {}".format(self.local))
        except socket.error:
            import sys
            print("Cannot setup the socket.", file=sys.stderr)
            sys.exit(-1)

    def send(self, data, sendTo, flag=0):
        pass

    def recv(self):
        pass

    def sendFile(self, filename, sendTo):
        print("start to send file: " + filename)
        # pack timestamp and filename
        start_time = time.time()

        # remove prefix
        bfilename = filename.split('/')[-1].encode('utf8')

        # send metadata
        self.send(bfilename, sendTo)
        for data in readFile(filename, chunk_size=DATA_LENGTH):
            self.send(data, sendTo)

        # end flag
        self.send(bytes(), sendTo, 2)
        end_time = time.time()
        print("\nTook {:.2f}s to transfer.".format(end_time - start_time))

    def recvFile(self):
        print("waiting for file")

        # unpack metadata
        received = self.recv()

        data = next(received)
        filename = data.decode('utf8')
        # start collect file chunks
        with open('saved/' + filename, 'wb') as dl:
            for data in received:
                dl.write(data)

        # deprecated: 
        #print("start_time: {}, end_time: {}".format(start_time, end_time))
        print("Received: {}.".format(filename))


    def teardown(self):
        try:
            self.localSocket.close()
        except:
            pass


class BasicUDPTransfer(BaseTransfer):
    """
    unreliable file transfer
    """
    def send(self, data, sendTo, flag=0):
        p = make_packet(0, data, flag=flag)
        self.localSocket.sendto(p, sendTo)

    def recv(self):
        # set time out to prevent it from blocking forever
        self.localSocket.settimeout(10)

        while True:
            try:
                message, address = self.localSocket.recvfrom(MAX_SIZE)
                _, _, _, flag, data = parse_packet(message)

                # simulate packet loss
                #if random.random() < self.prob_loss:
                #    print("packet loss!")
                #    continue
                yield data
                # last packet, don't wait for timeout
                if flag == 2:
                    break
            except socket.timeout:
                print('timeout. end.')
                break


class RDTTransfer(BaseTransfer):
    """
    reliable transfer by rdt3.0 over udp
    """
    def __init__(self, port=None, prob_loss=0.0):
        super().__init__(port, prob_loss=prob_loss)

        self.seq = 0

    def send(self, data, sendTo, flag=0):
        ack_received = False
        packet = make_packet(self.seq, data, flag)

        alpha = 0.875
        beta = 0.25
        ertt = 0.5
        devrtt = 0
        self.localSocket.settimeout(ertt)

        retrans = 0
        while not ack_received:
            start = time.time()
            self.localSocket.sendto(packet, sendTo)

            try:
                message, address = self.localSocket.recvfrom(MAX_SIZE)
            except socket.timeout:
                retrans += 1
                print('timeout, retrans = ' + str(retrans), end='\r')
            else:
                csum, rsum, seqnum, flag, data = parse_packet(message)

                # not corrupted and expected?
                if csum == rsum and seqnum == self.seq:
                    #print("ACK {} received.".format(self.seq))
                    end = time.time()
                    samplertt = end - start
                    ertt = alpha * ertt + (1-alpha) * samplertt
                    devrtt = (1-beta) * devrtt + beta * abs(samplertt - ertt)
                    self.localSocket.settimeout(ertt + 4 * devrtt)
                    ack_received = True
                else:
                    retrans += 1
                    print('timeout, retrans = ' + str(retrans), end='\r')
        self.seq = 1 - self.seq

    def recv(self):
        acks = 0
        nacs = 0

        self.localSocket.settimeout(60) # no one can wait for so long
        while True:
            try:
                message, address = self.localSocket.recvfrom(MAX_SIZE)

                csum, rsum, seqnum, flag, data = parse_packet(message)

                # check sum and seqnum
                if csum != rsum or seqnum != self.seq:
                    ACK = make_ack(1 - self.seq)
                    nacs += 1
                    self.localSocket.sendto(ACK, address)
                    print("acks: {}, NAK: {}.".format(acks, nacs), end='\r')
                else:
                    # simulate loss
                    if random.random() < self.prob_loss:
                        ACK = make_ack(1 - self.seq)
                        nacs += 1
                        self.localSocket.sendto(ACK, address)
                        print("acks: {}, NAK: {}.".format(acks, nacs), end='\r')
                        continue

                    # ack
                    ACK = make_ack(self.seq)
                    self.localSocket.sendto(ACK, address)
                    acks += 1
                    print("acks: {}, NAK: {}.".format(acks, nacs), end='\r')
                    self.seq = 1 - self.seq
                    yield data

                    # last packet, don't wait for more packets
                    if flag == 2:
                        print("\n last packet received.")
                        break
            except socket.timeout:
                print('timeout ? end.')
                break


class GBN(BaseTransfer):
    """
    Go-Back-N protocol
    """
    TIMEOUT = 0.2
    def __init__(self, local=None, prob_loss=0.0, window_size=10):
        super().__init__(local, prob_loss)
        self.window_size = window_size
        self.pkts = []
        self.nextseq = 0
        self.timer = 0.0

    def sendAll(self, sendTo):
        for pkt in self.pkts:
            self.localSocket.sendto(pkt, sendTo)

    def sendPkt(self, pkt, sendTo):
        self.pkts.append(pkt)
        self.localSocket.sendto(pkt, sendTo)
        self.nextseq = (self.nextseq + 1) & 0xffff
        if len(self.pkts) == 1:
            self.start_timer()

    def start_timer(self):
        self.timer = time.time()

    def send(self, data, sendTo, flag=0):
        unacked = len(self.pkts)
        packet = make_packet(self.nextseq, data, flag)
        oldest_unack = (self.nextseq - unacked) & 0xffff

        # fall back to fixed timeout value
        self.localSocket.settimeout(0.1)
        lastsent = False

        if flag == 2 and unacked < self.window_size:
            self.sendPkt(packet)
            lastsent = True

        while unacked >= self.window_size or (flag == 2 and unacked > 0):
            try:
                pkt, address = self.localSocket.recvfrom(MAX_SIZE)

            except socket.timeout:
                # resend all pkts
                if time.time() - self.timer < self.TIMEOUT:
                    self.start_timer()
                    self.sendAll(sendTo)
                    print("go back n, resend all")
            else:
                csum, rsum, seq, _, _ = parse_packet(pkt)

                # not corrupted
                if csum == rsum:
                    # cumulative acknowledgement
                    cum_acks = seq - oldest_unack + 1
                    if cum_acks < 0: # seqnum restarts from zero
                        cum_acks = seq + 1 + 0xffff - oldest_unack + 1
                    self.pkts = self.pkts[cum_acks:]
                    #print("seq: {}, oldest: {} cum ACK {}".format(seq, oldest_unack, cum_acks))
                    unacked -= cum_acks
                    oldest_unack = (oldest_unack + cum_acks) & 0xffff

                    if unacked != 0:
                        self.start_timer()

                    if flag == 2 and not lastsent:
                        self.sendPkt(packet, sendTo)
                        lastsent = True


        # ok to send now
        if flag != 2:
            self.sendPkt(packet, sendTo)


    def recv(self):
        acks = 0
        nacs = 0

        self.localSocket.settimeout(60) # no one can wait for so long
        while True:
            try:
                message, address = self.localSocket.recvfrom(MAX_SIZE)

                csum, rsum, seqnum, flag, data = parse_packet(message)

                # simulate loss
                if random.random() < self.prob_loss:
                    continue

                # check sum and seqnum
                if csum != rsum or seqnum != self.nextseq:
                    ACK = make_ack(self.nextseq - 1)
                    nacs += 1
                    self.localSocket.sendto(ACK, address)
                    print("acks: {}, NAK: {}.".format(acks, nacs), end='\r')
                else:
                    # ack
                    ACK = make_ack(self.nextseq)
                    self.localSocket.sendto(ACK, address)
                    acks += 1
                    print("acks: {}, NAK: {}.".format(acks, nacs), end='\r')
                    self.nextseq = (self.nextseq + 1) & 0xffff
                    yield data

                    # last packet, don't wait for more packets
                    if flag == 2:
                        print("\n last packet received.")
                        break
            except socket.timeout:
                print('timeout ? end.')
                break

class TCPTransfer(BaseTransfer):
    """
    Transfer via TCP
    """
    def __init__(self, port=None):
        self.port = port
        try:
            self.localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if port is not None:
                self.localSocket.bind(('', port))
                print("Successfully setup socket at port {}".format(port))
                self.localSocket.listen()
                print("localSocket starts to listen.")
        except socket.error as e:
            print(e)
            import sys
            print("Cannot setup the socket.", file=sys.stderr)
            sys.exit(-1)

        self.sent = 0

    def send(self, data, flag=0):
        packet = make_packet(0, data, flag)
        self.localSocket.send(packet)
        self.sent += 1
        #print("sent: {}".format(self.sent), end="\r")

    def recv(self):
        total = 0
        self.receiveSocket.settimeout(.1)
        while True:
            try:
                message = self.receiveSocket.recv(MAX_SIZE)
                _, _, _, flag, data = parse_packet(message)
                total += 1
                print("total: {} data: {}".format(total, len(data)), end="\r")
                if flag == 2 or not data:
                    break
                yield data
                # last packet, don't wait for timeout

            except socket.timeout:
                print('timeout. end.')
                break

    def sendFile(self, filename, sendTo):
        start_time = time.time()
        try:
            self.localSocket.connect(sendTo)
        except:
            print("Cannot connect to {}.".format(sendTo), file=sys.stderr)
            sys.exit(-1)

        print("start to send file: " + filename)

        # remove prefix
        bfilename = bytes(filename.split('/')[-1], 'utf8')
        l = len(bfilename).to_bytes(8, byteorder='big')
        padding = DATA_LENGTH - len(bfilename) - len(l)
        # send metadata
        self.send(l + bfilename + bytes(padding))

        for data in readFile(filename, chunk_size=DATA_LENGTH):
            self.send(data)

        # end flag
        self.send(bytes(DATA_LENGTH), flag=2)
        end_time = time.time()
        print("\nTook {:.2f}s to transfer.".format(end_time - start_time))

    def recvFile(self):
        try:
            self.receiveSocket, addr = self.localSocket.accept()
        except:
            print("error.", file=sys.stderr)
            sys.exit(-1)
        else:
            received = self.recv()
            data = next(received)
            fl_length = int.from_bytes(data[:8], byteorder='big')
            data = data[8:]
            filename = data[:fl_length].decode('utf8')
            with open('saved/' + filename, 'wb') as fl:
                for data in received:
                    fl.write(data)
            self.receiveSocket.close()
            print("\nReceived.")
