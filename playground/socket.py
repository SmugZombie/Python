import socket

server = socket.socket()
server.bind(('0.0.0.0', 50001))
server.listen(1)
conn, addr = server.accept()
print 'Connection established'

running = True
while running:
    try:
        data = conn.recv(4096)
    except KeyboardInterrupt:
        conn.close()
        running = False
    else:
        if data:
            print data
        else:
            conn.close()
            running = False
server.close()
