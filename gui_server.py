import socket
import threading
import math

header_size = 10
server_ip = "192.168.1.109"
port = int(input("Enter port: "))

print("")
type_of_encryption = input("[1] For Caesar Cipher\n[2] For Transposition Cipher\n[choice]: ")
number_of_connections = int(input("Enter number of connections: "))

clients_list = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(( server_ip, port ))
server.listen(number_of_connections)

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

def accept_and_print_and_send_messages(connected_client):

    while True:
        while True:
            new_message = True
            full_message = ""
            while True:
                message = connected_client.recv(1024).decode("utf-8")
                if new_message:
                    try:
                        message_size = int(message[:header_size])
                    except ValueError:
                        #accept_and_print_and_send_messages_thread.exit()
                        print("disconnected")
                        clients_list.remove(connected_client)
                        exit()
                    new_message = False
                full_message += message
                if len(full_message) - header_size == message_size:
                    accual_full_message = f"{full_message[header_size:]}"
                    print(f"\nemcrypted_message >> {accual_full_message}")
                    if str(type_of_encryption) == "1":
                        decrypted_message = caesar_cipther("decrypt", 10, accual_full_message)
                    elif str(type_of_encryption) == "2":
                        decrypted_message = transposition_cipher("decrypt", 5, accual_full_message)
                    print(f"decrypted_message >> {decrypted_message}\n")
                    full_message_to_send = f"{len(accual_full_message):<{header_size}}{accual_full_message}"
                    for clients in clients_list:
                        #if clients != connected_client:
                        clients.send(bytes(full_message_to_send, "utf-8"))
                    break
                break

def accept_clients():

    while True:
        client, address = server.accept()
        client.send(bytes(type_of_encryption, "utf-8"))
        clients_list.append(client)
        accept_and_print_and_send_messages_thread = threading.Thread(target = accept_and_print_and_send_messages, args = [client])
        accept_and_print_and_send_messages_thread.start()

accept_clients_thread = threading.Thread(target = accept_clients)
accept_clients_thread.start()
