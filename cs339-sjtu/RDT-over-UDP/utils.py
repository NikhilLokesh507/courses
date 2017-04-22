def checksum(data):
    """
    Calculate the modular sum of bytes data
    """
    return sum(data) & 0xff


def readFile(filename, chunk_size=256):
    with open(filename, 'rb') as fl:
        while True:
            chunk = fl.read(chunk_size)
            if not chunk:
                break
            yield chunk
