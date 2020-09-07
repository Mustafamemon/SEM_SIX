import socket			 

s = socket.socket()		 

# Define the port on which you want to connect 
port = 12345				
ip = '127.0.0.1'
s.connect((ip, port)) 
print(str(s.recv(1024),'utf-8'))
while True:
    ans = input('send message y/n : ')
    if ans == 'y' or ans == 'Y':
        data = input('Enter Message : ')
        s.send(bytes(data,'utf8'))
    elif ans == 'n' or ans == 'N':
        data ='n'      
        s.send(bytes(data,'utf8'))
        break
s.close()	 
