from transfer import BasicUDPTransfer
import sys

argv = sys.argv
if len(argv) != 5:
    print("usage: {} <protocol> <dest_host> <dest_port> <filename>".format(argv[0]))
    print("""
    protocol:
        basic    transfer using basic UDP socket
        rdt      rdt3.0
        sw       sliding window
    """)
    sys.exit()

dest_host = argv[2]
dest_port = int(argv[3])
filename  = argv[4]
prot = argv[1]

manager = None
if prot == 'basic':
    manager = BasicUDPTransfer(remote=(dest_host, dest_port))
else:
    pass


manager.sendFile(filename)
