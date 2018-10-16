import socket   # import socket module 
 
HOST,PORT = '127.0.0.1',8082 # host -> socket.gethostname() use to set machine IP  
 
my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
my_socket.bind((HOST,PORT))
my_socket.listen(1)

while True:
    connection,address = my_socket.accept()
    req = connection.recv(1024).decode('utf-8')
    print(req) # Get print in our python console.