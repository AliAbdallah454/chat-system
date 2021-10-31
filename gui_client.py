import socket
import threading
import math
from tkinter import *

#encryption

def caesar_cipther(mode, key, text):

    symbols = "1QAZ$3EDC5!TGB7.UJM9OLP2WSXRFVYHN8I:>Kqaz#wsx 4edcrfv,tgby6hnujmiko0lp"
    full_encrypted_decrypted_message = ""

    for letter in text:
        if letter in symbols:
            letter_index = symbols.find(letter)

            if mode == "encrypt":
                encrypted_letter_index = letter_index + key
            elif mode == "decrypt":
                encrypted_letter_index = letter_index - key

            if encrypted_letter_index >= len(symbols):
                encrypted_letter_index = encrypted_letter_index - len(symbols)
            elif encrypted_letter_index < 0:
                encrypted_letter_index = encrypted_letter_index + len(symbols)

            full_encrypted_decrypted_message += symbols[encrypted_letter_index]
        else:
            full_encrypted_decrypted_message += letter

    return full_encrypted_decrypted_message

def transposition_cipher(mode, key, text):

    if mode == "encrypt":
        cipher_list = [""] * key

        for column in range(key):
            current_index = column

            while current_index < len(text):
                cipher_list[column] += text[current_index]
                current_index += key

        full_encrypted_decrypted_message = "".join(cipher_list)
        return full_encrypted_decrypted_message

    elif mode == "decrypt":
        number_of_rows = key
        number_of_columns = int(math.ceil( len(text)/float(key) ))
        number_of_shaded_boxes = (number_of_columns * number_of_rows) - len(text)

        column = 0
        row = 0

        cipher_list = [""] * number_of_columns

        for letter in text:
            cipher_list[column] += letter
            column += 1

            if (column == number_of_columns) or (column == number_of_columns - 1 and row >= number_of_rows - number_of_shaded_boxes):
                column = 0
                row += 1

        full_encrypted_decrypted_message = "".join(cipher_list)
        return full_encrypted_decrypted_message

#encryption

is_accepted = True
header_size = 10
server_ip = "83.136.252.243"
port = int(input("Enter port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(( server_ip, port ))

type_of_encryption = client.recv(1024).decode("utf-8")
name = input("Enter name: ")

#tkinter

def send_message():
    message = message_entry.get()
    if str(type_of_encryption) == "1":
        encrypted_message_with_name = caesar_cipther("encrypt", 10, f"{name} >>: {message}")
    elif str(type_of_encryption) == "2":
        encrypted_message_with_name = transposition_cipher("encrypt", 5, f"{name}>>:{message}")
    message_to_send = f"{len(encrypted_message_with_name):<{header_size}}{encrypted_message_with_name}"
    client.send(bytes(message_to_send, "utf-8"))
    message_entry.delete(0, END)

#tkinter

def accept_and_print_messages():
    while True:
        while True:
            new_message = True
            full_received_message = ""
            while True:
                received_message = client.recv(1024).decode("utf-8")
                if new_message:
                    received_message_size = int(received_message[:header_size])
                    new_message = False
                full_received_message += received_message
                if len(full_received_message) - header_size == received_message_size:
                    accual_full_message_received = f"{full_received_message[header_size:]}"
                    if str(type_of_encryption) == "1":
                        decrypted_message = caesar_cipther("decrypt", 10, accual_full_message_received)
                    elif str(type_of_encryption) == "2":
                        decrypted_message = transposition_cipher("decrypt", 5, accual_full_message_received)
                    print(f"{decrypted_message}")
                    text_field.insert(INSERT, f"{decrypted_message}\n")
                    break
                break

if is_accepted:
    accept_and_print_messages_thread = threading.Thread(target = accept_and_print_messages)
    accept_and_print_messages_thread.start()

    root = Tk()

    message_entry = Entry(root, width = 145, borderwidth = 10, font = ("Helvetica", "10", "bold italic"))
    message_entry.grid(column = 0, row = 0)
    send_button = Button(root, text = "send", width = 8, borderwidth = 8, command = send_message)
    send_button.grid(column = 1, row = 0)
    text_field = Text(root, width = 145, borderwidth = 10, font = ("Helvetica", "10", "bold italic"))
    text_field.grid(column = 0, row = 1)
    name_label = Label(root, text = name, width = 5, font = ("Helvetica", "10", "bold italic"))
    name_label.grid(column = 1, row = 1)

    root.mainloop()
else:
    print("opsidonpi, wrong password :)")
