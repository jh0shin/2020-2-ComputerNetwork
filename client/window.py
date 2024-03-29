from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import client
 
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
 
port = 8000
 
class CWidget(QWidget):
    def __init__(self):
        super().__init__()  
         
        self.c = client.ClientSocket(self)
        
        self.initUI()
 
    def __del__(self):
        self.c.stop()
 
    def initUI(self):
        self.setWindowTitle('클라이언트')
         
        # 클라이언트 설정 부분
        ipbox = QHBoxLayout()
 
        gb = QGroupBox('서버 설정')
        ipbox.addWidget(gb)
 
        box = QHBoxLayout()
 
        label = QLabel('Server IP')
        self.ip = QLineEdit('192.168.56.1')
        self.ip.setInputMask('000.000.000.000;_')
        box.addWidget(label)
        box.addWidget(self.ip)
 
        label = QLabel('Server Port')
        self.port = QLineEdit(str(port))
        box.addWidget(label)
        box.addWidget(self.port)

        name = QLabel('사용자 이름')
        self.name = QLineEdit()
        box.addWidget(name)
        box.addWidget(self.name)
 
        self.btn = QPushButton('접속')       
        self.btn.clicked.connect(self.connectClicked)
        box.addWidget(self.btn)
 
        gb.setLayout(box)       
 
        # 채팅창 부분  
        infobox = QHBoxLayout()      
        gb = QGroupBox('메시지')        
        infobox.addWidget(gb)
 
        box = QVBoxLayout()
         
        label = QLabel('받은 메시지')
        box.addWidget(label)
 
        self.recvmsg = QListWidget()
        box.addWidget(self.recvmsg)
 
        label = QLabel('보낼 메시지')
        box.addWidget(label)
 
        self.sendmsg = QTextEdit()
        self.sendmsg.setFixedHeight(50)
        box.addWidget(self.sendmsg)
 
        hbox = QHBoxLayout()
 
        box.addLayout(hbox)
        self.sendbtn = QPushButton('보내기')
        self.sendbtn.setAutoDefault(True)
        self.sendbtn.clicked.connect(self.sendMsg)

        self.sendfilebtn = QPushButton('파일 보내기')
        self.sendfilebtn.setAutoDefault(True)
        self.sendfilebtn.clicked.connect(self.sendFile)
 
        hbox.addWidget(self.sendbtn)
        hbox.addWidget(self.sendfilebtn)
        gb.setLayout(box)
 
        # 전체 배치
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)       
        vbox.addLayout(infobox)
        self.setLayout(vbox)
         
        self.show()
 
    def connectClicked(self):
        if self.c.bConnect == False:
            ip = self.ip.text()
            port = self.port.text()
            if self.c.connectServer(ip, int(port)):
                self.btn.setText('접속 종료')
            else:
                self.c.stop()
                self.sendmsg.clear()
                self.recvmsg.clear()
                self.btn.setText('접속')
        else:
            self.c.stop()
            self.sendmsg.clear()
            self.recvmsg.clear()
            self.btn.setText('접속')
 
    def updateMsg(self, msg):
        self.recvmsg.addItem(QListWidgetItem(msg))
 
    def updateDisconnect(self):
        self.btn.setText('접속')
 
    def sendMsg(self):
        sendmsg = "[" +self.name.text() + "]: " + self.sendmsg.toPlainText()       
        self.c.send(sendmsg, False)        
        self.sendmsg.clear()

    def sendFile(self):
        sendfilename = self.sendmsg.toPlainText()
        self.c.send(sendfilename, True)
        self.sendmsg.clear()
 
    def closeEvent(self, e):
        self.c.stop()       
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())