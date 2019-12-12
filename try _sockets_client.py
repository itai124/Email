import  socket
import  pickle
BUFSIZ = 1024
HOST = 'localhost'
PORT = 50008
ADDR = (HOST, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
while True:
    data = ['x','y','g','t']
    updated= pickle.dumps(data)
    client_socket.send(updated)
    data = client_socket.recv(BUFSIZ)
    print pickle.loads(data)
    client_socket.send(data)
client_socket.close()