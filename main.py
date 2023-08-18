from tkinter import *
from tkinter import messagebox
import base64

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def save_and_encrypt_notes():
    title = title_entry.get()
    massage = input_text.get("1.0",END)
    master_secret = input_master_secret.get()

    if len(title) == 0 or len(massage) == 0 or len(master_secret) == 0:
        messagebox.showwarning('Error!','Please enter all info')
    else:
        #encryption
        massage_encrypted = encode(master_secret,massage)
        try:
            with open("mysecret.txt", "a") as data_file:
                data_file.write(f"\n{title}\n{massage_encrypted}")
        except FileNotFoundError:
           with open("mysecret.txt", "w") as data_file:
               data_file.write(f"\n{title}\n{massage_encrypted}")
        finally:
           title_entry.delete(0,END)
           input_master_secret.delete(0,END)
           input_text.delete("1.0",END)

def decrypt_notes():
    message_encrypted = input_text.get("1.0",END)
    master_secret = input_master_secret.get()

    if len(message_encrypted) == 0 or len(master_secret)== 0:
        messagebox.showwarning('Error!','Please enter all info')
    else:
        try:
            decrypted_message = decode(master_secret, message_encrypted)
            input_text.delete("1.0",END)
            input_text.insert("1.0",decrypted_message)
        except:
            messagebox.showerror('Error!','Plase enter encrypted text!')
#UI
FONT = ("Verdana",11,"normal")
window = Tk()
window.title("Secret Notes")
window.config(pady=30,padx=30)

photo = PhotoImage(file="topsecret.png")
photo_label = Label(image=photo,bg="#D6D614")
photo_label.pack()

title_info_label = Label(text="Enter Your Title",font=FONT)
title_info_label.pack()

title_entry = Entry(width=30)
title_entry.pack()

input_info_label = Label(text="Enter Your Secret",font=FONT)
input_info_label.pack()

input_text = Text(width=33,height=18)
input_text.pack()

master_secret_label = Label(text="Enter Master Key",font=FONT)
master_secret_label.pack()

input_master_secret = Entry(width=30)
input_master_secret.pack()

save_button = Button(text= "Save and Encrypt",command=save_and_encrypt_notes)
save_button.pack()

decrypt_button = Button(window,text="Decrypt",command=decrypt_notes)
decrypt_button.pack()

window.mainloop()