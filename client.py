#!/usr/bin/env python3

import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 4:
    print("Script, IP address, port, key")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
shift = int(sys.argv[3])
server.connect((IP_address, Port))

def decrypt(message):
    encryptedm = ""
    for m in message:
        if m.isupper():
            c_unicode = ord(m)
            c_index = ord(m) - ord("A")
            new_index = (c_index - shift) % 26
            new_unicode = new_index + ord("A")
            new_char = chr(new_unicode)
            encryptedm = encryptedm + new_char
        elif m.islower():
            c_unicode = ord(m)
            c_index = ord(m) - ord("a")
            new_index = (c_index - shift) % 26
            new_unicode = new_index + ord("a")
            new_char = chr(new_unicode)
            encryptedm = encryptedm + new_char
        else:
            encryptedm +=m
    return encryptedm
while True:
    socket_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(socket_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(decrypt(message.decode()))
        else:
            message = sys.stdin.readline()
            encryptedm = ""
            for m in message:
                if m.isupper():
                    c_unicode = ord(m)
                    c_index = ord(m) - ord("A")
                    new_index = (c_index + shift) % 26
                    new_unicode = new_index + ord("A")
                    new_char = chr(new_unicode)
                    encryptedm = encryptedm + new_char
                elif m.islower():
                    c_unicode = ord(m)
                    c_index = ord(m) - ord("a")
                    new_index = (c_index + shift) % 26
                    new_unicode = new_index + ord("a")
                    new_char = chr(new_unicode)
                    encryptedm = encryptedm + new_char
                else: 
                    encryptedm += m
            server.send(encryptedm.encode())
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()