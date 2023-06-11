import tkinter as tk
import subprocess
import threading
import queue
import aes_decrypt

# 定義一個 Queue 來傳遞訊息
message_queue = queue.Queue()


def UpdateUI(status, token, username):
    print("Updating UI...")
    import loadFromPhoneMSG
    encrypted_hex = loadFromPhoneMSG.getencrypted()
    ivhex = loadFromPhoneMSG.getivhexData()
    tokenvalue = aes_decrypt.aes_256_cbc_decrypt(ivhex, encrypted_hex)
    # 更改status、token和username的顯示值
    status.set("Status: Connection")
    token.set("Token:", tokenvalue)
    username.set("Username: myid")


def rfserver():
    print("rf-server running")
    # Note: 在此處，我們需要考慮如何將 message_queue 傳遞給檔案B
    subprocess.run(['python3', 'rf-server.py'])


def check_rfserver_status(root, status, token, username):
    try:
        # 嘗試從 Queue 取出訊息
        message = message_queue.get_nowait()
        # 如果有訊息，調用 UpdateUI 函數
        if message == "File saved":
            UpdateUI(status, token, username)
    except queue.Empty:
        pass
    # 每秒檢查一次
    root.after(1000, check_rfserver_status, root, status, token, username)


def button_clicked():
    print("Button Clicked")
    # 更改username_label的text
    username.set("Username: new_user")


# init
root = tk.Tk()
username = tk.StringVar()
username.set("Username:")
status = tk.StringVar()
status.set("Status:disconnection")
token = tk.StringVar()
token.set("Token:")

username_label = tk.Label(root, textvariable=username)
username_label.pack()
status_label = tk.Label(root, textvariable=status)
status_label.pack()
token_label = tk.Label(root, textvariable=token)
token_label.pack()

button = tk.Button(root, text="Click me", command=button_clicked)
button.pack()

# 使用 thread 執行 rfserver 函數，使其在背景運行
rfserver_thread = threading.Thread(target=rfserver)
rfserver_button = tk.Button(root, text="Second Button", command=rfserver_thread.start)
rfserver_button.pack()

# 開始檢查 rfserver 的狀態
check_rfserver_status(root, status, token, username)

root.mainloop()
