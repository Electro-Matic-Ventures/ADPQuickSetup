import socket
from codecs import decode

IP_ADDRESS = input("Enter sign IP ADDRESS > ")
PORT = int(input("Enter a port number > "))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((IP_ADDRESS, PORT))

print(" ")
argv = " "

while True:
    argv = input("Enter a string > ")
    data = decode("01", "hex") + "Z00".encode() + decode("02", "hex") + f"AA{argv}".encode() + decode("04", "hex")
    s.sendall(data)

s.close()
