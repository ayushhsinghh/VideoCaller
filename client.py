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
            
                cv2.imshow('TRANSMITTING VIDEO',frame)
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
        frame = imutils.resize(frame,height=1020,width=640)
        cv2.imshow("RECEIVING VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            break
    client_socket.close()
    cv2.destroyAllWindows()
    
    
# Connect with Server
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.0.105' #IP Address of Host to be Entered 
port = 9999
client_socket.connect((host_ip,port))

url = 0
x1=threading.Thread(target=recieve)
x2=threading.Thread(target=transmit , args=(url,))
x1.start()
x2.start()