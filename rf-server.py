import bluetooth
import threading
import queue
import base64
import binascii

token_queue = queue.Queue()  # Global variable to store tokens

def save_string_to_file(filename, content):
    with open(filename, "w+") as file:
        file.write(content)

def handle_client(sock, client_info):
    print("Accepted connection from", client_info)
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            
            if len(data) > 10:
                try:
                    decoded_data = base64.b64decode(data.decode('utf-8'))  # Perform base64 decoding
                    token_queue.put(decoded_data)  # Put decoded_data into the queue
                except binascii.Error:
                    decoded_data = data  # Use original data if decoding fails
                
                decoded_data_str = str(decoded_data)[2:-1]  # Convert to string and remove leading "b'" and trailing "'"
                print("Received", decoded_data_str)
                filename = "FromPhoneMSG.txt"
                save_string_to_file(filename, decoded_data_str)
            else:
                data_str = data.decode('utf-8')  # Convert bytes to string
                print("Received", data_str)
                filename = "FromPhoneMSG.txt"
                save_string_to_file(filename, data_str)
                
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

    # Get tokens in the main thread
    while not token_queue.empty():
        token = token_queue.get()
        print("Token from client:", token)

server_sock.close()
print("All done.")
