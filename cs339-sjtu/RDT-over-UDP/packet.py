from utils import checksum


def parse_packet(data):
    csum = checksum(data[1:])
    seqnum = int.from_bytes(data[1:3], byteorder='big')
    flag = int.from_bytes(data[3:4], byteorder='big')
    data = data[4:]

    return csum, seqnum, flag, data


class Packet:
    """
    The packet class.
    Consists of:
    1. checksum  (1 bytes)
    2. seqnum    (2 bytes) reserved 2 bytes
    3. flag      (1 bytes)  # first packet 0, packet 1, last packet 2
    4. data      (1020 bytes) # at most 1020 bytes


    A single packet will not exceed 1024 bytes.
    """
    DATA_LENGTH = 1020

    def __init__(self, seqnum, data, flag=0):
        """
        create a packet from its metadata and data
        """
        if len(data) > Packet.DATA_LENGTH:
            import sys
            print("Abort: packet size exceeds maximum size.", file=sys.stderr)
            sys.exit(-1)

        self.seqnum = seqnum
        self.data = data
        self.flag = flag

    def __bytes__(self):
        """
        return a bytes representation for transfer
        """
        packet_content = (self.seqnum.to_bytes(2, byteorder='big') +
                          self.flag.to_bytes(1, byteorder='big') +
                          self.data)
        csum = checksum(packet_content)
        return csum.to_bytes(1, byteorder='big') + packet_content


if __name__ == '__main__':
    data = bytes('hello, kevin', 'utf8')
    p = Packet(17, data, 2)
    bs = bytes(p)
    print(bs)
    print(parse_packet(bs))
