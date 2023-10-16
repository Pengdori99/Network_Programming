import tkinter as tk
import cv2
import socket
import threading
from PIL import Image, ImageTk

# 서버 설정------------------------------------------------------------------------------
server_host = ''  # 서버의 IP 주소
server_port = 12345 # 포트 번호

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 주소와 포트에 바인딩
server_socket.bind((server_host, server_port))

# 클라이언트 연결
server_socket.listen(1)
sock, addr = server_socket.accept()

print(addr[0],addr[1])
print(f"서버가 {server_host}:{server_port} 에서 실행 중입니다.")
#---------------------------------------------------------------------------------------------------

# 화면 갱신 함수
def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
    window.after(10, update)

# 메시지 보내기 함수
def send_message():
    message = entry.get()
    sock.send(message.encode('utf-8'))
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "나: " + message + "\n")
    chat_text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)


#-------------------------------------------------------------------------------------------------
t1 = threading.Thread(target=update)
t2 = threading.Thread(target=send_message)

t1.start()
t2.start()
#-------------------------------------------------------------------------------------------------


# GUI 초기화
window = tk.Tk()
window.title("Chan의 화상 채팅")

# 웹캠 초기화
cap = cv2.VideoCapture(0)

# 라벨 위젯을 사용하여 영상 표시 (80%)
label = tk.Label(window)
label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

# 채팅 창 (Text 위젯) 추가 (20%)
chat_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 입력 필드 (20%)
entry = tk.Entry(window)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 보내기 버튼 (20%)
send_button = tk.Button(window, text="보내기", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

# 행 및 열 가중치 설정
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=10)  # 비디오 화면이 80% 차지
window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

# 갱신 함수 호출
update()

# GUI 시작
window.mainloop()

# 웹캠 해제
cap.release()