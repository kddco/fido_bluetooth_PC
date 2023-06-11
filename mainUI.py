# 檔案A
import tkinter as tk
import subprocess
import threading
import aes_decrypt
def removenotifiyflag():
    import os

    file_path = "notification.txt"

    try:
        os.remove(file_path)
        print(f"The file '{file_path}' has been successfully removed.")
    except FileNotFoundError:
        print(f"File '{file_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied. Unable to remove the file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while trying to remove the file '{file_path}': {str(e)}")


def UpdateUI(status, token, username):
    print("Updating UI...")
    import loadFromPhoneMSG
    encrypted_hex = loadFromPhoneMSG.getencrypted()
    ivhex = loadFromPhoneMSG.getivhexData()
    tokenvalue = aes_decrypt.aes_256_cbc_decrypt(ivhex, encrypted_hex)
    # 更改status、token和username的顯示值
    status.set(f"Status: Connection")
    token.set(f"Token: {tokenvalue}")
    username.set(f"Username: myid")


def rfserver():
    print("rf-server running")
    subprocess.run(['python3', 'rf-server.py'])


def check_rfserver_status(root, status, token, username):
    try:
        # 檢查通知文件
        with open("notification.txt", "r") as file:
            message = file.read().strip()
            # 如果有訊息，調用 UpdateUI 函數
            if message == "File saved":
                UpdateUI(status, token, username)
                removenotifiyflag()
    except FileNotFoundError:
        pass
    # 每秒檢查一次
    root.after(1000, check_rfserver_status, root, status, token, username)


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

button = tk.Button(root, text="Click me", command=lambda: threading.Thread(target=rfserver).start())
button.pack()
removenotifiyflag()
# 開始檢查 rfserver 的狀態
check_rfserver_status(root, status, token, username)

root.mainloop()
