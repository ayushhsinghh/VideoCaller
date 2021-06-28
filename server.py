import socket, cv2, pickle, struct, imutils ,threading

def transmit(url):
    while True:
        if client_socket:
            vid = cv2.VideoCapture(url)
            while(vid.isOpened()):
                img,frame = vid.read()
                frame = imutils.resize(frame,width=200)
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
            
                cv2.imshow('TO CLIENT',frame)
                key = cv2.waitKey(1) & 0xFF
                if key ==ord('q'):
                    client_socket.close()
                    break
    cv2.destroyAllWindows()

def recieve():
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024) 
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        frame = imutils.resize(frame,width=720)
        cv2.imshow("FROM CLIENT",frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            break
    client_socket.close()
    cv2.destroyAllWindows()
    

# Create Socket to connect to Client
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = '192.168.0.105'
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)
# Socket Bind
server_socket.bind(socket_address)
server_socket.listen(5)
print("LISTENING AT:",socket_address)
client_socket,addr = server_socket.accept()
print('GOT CONNECTION FROM:',addr)



url = 'http://192.168.0.192:8080/video'
x1=threading.Thread(target=transmit , args=(url,))
x2=threading.Thread(target=recieve)
x1.start()
x2.start()
