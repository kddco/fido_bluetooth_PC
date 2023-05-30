import bluetooth
import threading
import queue
import base64
import binascii

token_queue = queue.Queue()  # 全域變數，用來儲存 token

def handle_client(sock, client_info):
    print("Accepted connection from", client_info)
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            data_str = data.decode('utf-8')  # 將 bytes 轉換為字串
            try:
                decoded_data = base64.b64decode(data_str)  # 進行 base64 decode
                token_queue.put(decoded_data)  # 將 decoded_data 放入 queue
            except binascii.Error:
                decoded_data = data_str  # 直接使用原始數據
            print("Received", decoded_data)
            
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

    # 在主線程中取得 token
    while not token_queue.empty():
        token = token_queue.get()
        print("Token from client:", token)

server_sock.close()
print("All done.")
