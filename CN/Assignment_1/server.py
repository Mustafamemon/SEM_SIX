import socket			 

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)		 
print("Socket successfully created")

port = 12345				
ip  = '127.0.0.1'

s.bind((ip, port))		 
print("socket binded to " ,port)

s.listen(5)	 
print ("socket is listening")			

try:
    while True:   
        c, addr = s.accept()
        print ('Got connection from', addr)
        c.send(b'Thank you for connecting') 
        while True: 
            data  = str(c.recv(1024),'utf-8')
            if  data == 'N' or data == 'n':
                c.close()
                break
            print(data)
except (KeyboardInterrupt):
    s.close()

    

 
