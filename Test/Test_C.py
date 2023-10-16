import socket

# 서버 설정
server_host = '127.0.0.1'  # 서버의 IP 주소
server_port = 12345       # 서버 포트 번호

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((server_host, server_port))

# 서버에 메시지 보내고 응답 받기
while True:
    message = input("서버에게 보낼 메시지: ")
    client_socket.send(message.encode('utf-8'))

    if message.lower() == 'exit':
        break

    response = client_socket.recv(1024).decode('utf-8')
    print(f"서버로부터 받은 응답: {response}")

# 연결 종료
client_socket.close()
