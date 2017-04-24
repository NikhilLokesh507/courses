from transfer import *
import sys

argv = sys.argv
if len(argv) < 3:
    print("usage:python3 {} <protocol> <port> [<prob_loss>]".format(argv[0]))
    print("""
    protocol:
        udp      transfer using basic UDP socket
        rdt      rdt3.0
        GBN      Go-Back-N (20)

    prob_loss: probability to drop a packet (simulate network), optional, defaults to 0
    """)
    sys.exit()

port = int(argv[2])
prot = argv[1]
prob_loss = 0.0
if len(argv) > 3:
    prob_loss = float(argv[3])
manager = None
if prot == 'udp':
    manager = BasicUDPTransfer(port, prob_loss)
elif prot == 'rdt':
    manager = RDTTransfer(port, prob_loss)
elif prot == 'GBN':
    manager = GBN(port, prob_loss)
else:  # TCP
    manager = TCPTransfer(port)


manager.recvFile()

manager.teardown()
