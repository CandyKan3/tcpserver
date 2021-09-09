#!/usr/bin/env python3

import socket
import json
import select
import sys
import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 4:
    print("Script, IP address, port, key")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
password = str(sys.argv[3])
server.connect((IP_address, Port))


def get_private_key(password):
    salt = b"this is a salt phrase"
    kdf = PBKDF2(password, salt, 64, 100)
    key = kdf[:32]
    return key


def encrypt(raw, password):
    private_key = get_private_key(password)
    key = private_key
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return (ciphertext, tag, nonce)


def decrypt(enc, password, tag, nonce):
    private_key = get_private_key(password)
    cipher = AES.new(private_key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(enc)
    try:
        cipher.verify(tag)
        print("Message is authentic: ", plaintext)
    except ValueError:
        print("Key incorrect or message corrupted")


while True:
    socket_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(
        socket_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            messagetag = message[:50]
            print(messagetag ," TAG")

        else:
            message = sys.stdin.readline()
            cypher, tag, nonce = encrypt(message, password)
            print(tag+cypher)
            server.send(tag + cypher)
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()
