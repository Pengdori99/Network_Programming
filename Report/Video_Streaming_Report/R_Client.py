import tkinter as tk
import threading
import cv2
import socket
import numpy as np
from PIL import Image, ImageTk

# 서버 IP 주소 및 포트 번호
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((SERVER_IP, SERVER_PORT))

# 웹캠 캡처를 위한 스레드
class VideoStreamThread(threading.Thread):
    def __init__(self, server_socket):
        super().__init__()
        self.server_socket = server_socket

    def run(self):
        cap = cv2.VideoCapture(0)  # 웹캠 캡처
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()
            self.server_socket.sendall(img_bytes)

# 클라이언트 소켓 설정
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# GUI 생성
root = tk.Tk()
root.title("Video Streaming Client")

# 비디오 프레임 표시
frame = tk.Label(root)
frame.pack()

# 서버로부터 비디오 스트리밍을 받아 화면에 표시하는 함수
def receive_video_stream():
    while True:
        try:
            img_bytes = client_socket.recv(1024)
            img_encoded = np.frombuffer(img_bytes, dtype=np.uint8)
            frame = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            frame_label.config(image=photo)
            frame_label.image = photo
        except Exception as e:
            print(e)
            break

# 비디오 수신 스레드 시작
video_thread = threading.Thread(target=receive_video_stream)
video_thread.daemon = True
video_thread.start()

# 메시지 전송 함수

# while True:
#     message = input("서버에게 보낼 메시지: ")
#     client_socket.send(message.encode('utf-8'))
#
#     if message.lower() == 'exit':
#         break
#
#     response = client_socket.recv(1024).decode('utf-8')

def send_message():
    message = entry.get()
    client_socket.sendall(message.encode())
    entry.delete(0, tk.END)


# GUI 구성요소 생성
entry = tk.Entry(root, width=50)
entry.pack()
# 채팅 창 (Text 위젯) 추가 (20%)
chat_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

# GUI 시작
root.mainloop()
def send_C():
    while True:
        message = input("서버에게 보낼 메시지: ")
        client_socket.send(message.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        chat_text.insert(tk.END, response)

t1 = threading.Thread(target=send_message)
# t2 = threading.Thread(target=send_C)
t1.start()
# t2.start()

t1.join()
t2.join()
# 연결 종료 시 스레드 및 소켓 닫기
# client_socket.close()