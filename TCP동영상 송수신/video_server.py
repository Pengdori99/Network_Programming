import socket
import cv2
import pickle
import struct
import imutils

#소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9000
server_addr = ('',port)

server_socket.bind(server_addr)

server_socket.listen(5)
print("접속대기", server_addr)

while True:
    client_socket, addr = server_socket.accept()
    print(addr, '와 연결됨')
    if client_socket:
        vid = cv2.VideoCapture(0)
        if vid.isOpened():
            print(vid.get(3),vid.get(4))
        while vid.isOpened():
            img, frame = vid.read()
            frame = imutils.resize(frame,width=640)
            frame_bytes = pickle.dumps(frame)
            msg = struct.pack("Q",len(frame_bytes)) + frame_bytes

            client_socket.sendall(msg)

            cv2.imshow('',frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()