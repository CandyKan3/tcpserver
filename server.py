#!/usr/bin/env python3
import socket
import select
import sys
from _thread import *

HOST = '127.0.0.1'
PORT = 8081
shift = 3
def encrypt(message):
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
            encryptedm +=m
    return encryptedm   
def decrypt(message):
    encryptedm = message
    return encryptedm 
def clientthread(conn, addr):
    conn.send(encrypt("Welcome to the chatroom!").encode())
    while True:
        try:
            message = conn.recv(2048)
            print("Message here" + message.decode())
            if message:
                print("<"+ addr[0] + ">: "+ decrypt(message.decode()))
                message_to_send = "<"+ addr[0] + ">"+ message.decode()
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(100)
    list_of_clients = []
    while True:
        conn, addr = s.accept()
        list_of_clients.append(conn)
        print(addr[0]+ "Connected")
        start_new_thread(clientthread,(conn,addr))
    conn.close()
