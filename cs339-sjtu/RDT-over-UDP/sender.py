from transfer import *
import sys

argv = sys.argv
if len(argv) != 5:
    print("usage:python3 {} <protocol> <dest_host> <dest_port> <filename>".format(argv[0]))
    print("""
    protocol:
        udp       transfer using basic UDP socket
        rdt       rdt3.0
        GBN       sliding window
        tcp       tcp
    """)
    sys.exit()

dest_host = argv[2]
dest_port = int(argv[3])
filename  = argv[4]
prot = argv[1]
sendTo = (dest_host, dest_port)
manager = None
if prot == 'udp':
    manager = BasicUDPTransfer()
elif prot == 'rdt':
    manager = RDTTransfer()
elif prot == 'GBN':
    manager = GBN(window_size=10)
else: # tcp
    manager = TCPTransfer()


manager.sendFile(filename, sendTo)

manager.teardown()
