from PySide2.QtWidgets import *
from PySide2.QtGui import *
import socket
import threading

listenSocket : socket    
clients = []    

def start():
    startButton.setEnabled(False)
    threading._start_new_thread(handleCalc,())

def handleCalc():
    IP = '127.0.0.1'
    PORT = 8088
    global listenSocket
    listenSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
    listenSocket.bind((IP,PORT))
    listenSocket.listen(10)                                          
    message.insertPlainText('等待连接\n')                        
    while True:
        client = listenSocket.accept()                          
        t = threading.Thread(target=recv,args=(client,))  
        t.start()                                           

def recv(client):
    global clients
    cont= client[0].recv(1024).decode()                   
    message.insertPlainText(f'{cont}连接成功\n')    
    clients.append(client[0])  
    while True:
        msg = client[0].recv(1024).decode()
        message.insertPlainText(f'客户机：{msg}/')                               

def send():
    msg = textEdit.toPlainText()          
    message.insertPlainText(msg+'\n')
    textEdit.setPlainText('')              
    global clients
    for client in clients:                
        client.send(msg.encode())

app = QApplication([])
window = QMainWindow()
window.resize(1000,800)
window.move(300,300)
window.setWindowTitle('Message Server')


label1 = QLabel(window)
label1.move(50,10)

label2 = QLabel(window)
label2.move(50,560)

label3 = QLabel(window)
label3.move(700,10)

message = QPlainTextEdit(window)
message.move(50,50)
message.resize(650,500)
message.setReadOnly(True)

textEdit = QPlainTextEdit(window)
textEdit.move(50,600)
textEdit.resize(650,100)

startButton = QPushButton('开始',window)
startButton.move(700,350)
startButton.clicked.connect(start)

sendButton = QPushButton('发送',window)
sendButton.move(700,600)
sendButton.clicked.connect(send)

window.show()
app.exec_()
