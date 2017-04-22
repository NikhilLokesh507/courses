from transfer import BasicUDPTransfer

but = BasicUDPTransfer(local=('localhost', 12345))
but.recvFile()
