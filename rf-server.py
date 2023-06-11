import bluetooth
import threading
import queue
import base64
import binascii

token_queue = queue.Queue()  # 全局变量，用来存储 token

def save_string_to_file(filename, content):
    with open(filename, "w+") as file:
        file.write(content)
        file.close()

def handle_client(sock, client_info):
    print("Accepted connection from", client_info)
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            data_str = data.decode('utf-8')  # 将 bytes 转换为字符串
            try:
                decoded_data = base64.b64decode(data_str)  # 进行 base64 解码
                token_queue.put(decoded_data)  # 将 decoded_data 放入队列
            except binascii.Error:
                decoded_data = data_str  # 直接使用原始数据
            decoded_data_str = str(decoded_data)[2:-1]  # 转换为字符串并去除开头的"b'"和结尾的"'"
            print("Received", decoded_data_str)
            filename = "FromPhoneMSG.txt"
            content = decoded_data_str
            save_string_to_file(filename, content)
    except OSError:
        pass

    print(f"Disconnected from {client_info}.")
    sock.close()

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
print("Waiting for connection on RFCOMM channel", port)

while True:
    client_sock, client_info = server_sock.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_sock, client_info))
    client_thread.start()

    # 在主线程中获取 token
    while not token_queue.empty():
        token = token_queue.get()
        print("Token from client:", token)

server_sock.close()
print("All done.")
