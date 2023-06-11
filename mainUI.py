import tkinter as tk
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
token_label = tk.Label(root, text=token)
token_label.pack()

button = tk.Button(root, text="Click me", command=button_clicked)
button.pack()

root.mainloop()

