from threading import *
from socket import *
from PyQt5.QtCore import Qt, pyqtSignal, QObject

# file sending
from os.path import exists
import os
import sys
 
class Signal(QObject):  
    recv_signal = pyqtSignal(str)
    disconn_signal = pyqtSignal()   
 
class ClientSocket:
 
    def __init__(self, parent):        
        self.parent = parent                
        
        self.recv = Signal()        
        self.recv.recv_signal.connect(self.parent.updateMsg)
        self.disconn = Signal()        
        self.disconn.disconn_signal.connect(self.parent.updateDisconnect)
 
        self.bConnect = False
         
    def __del__(self):
        self.stop()
 
    def connectServer(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)           
 
        try:
            self.client.connect( (ip, port) )
        except Exception as e:
            print('Connect Error : ', e)
            return False
        else:
            self.bConnect = True
            self.t = Thread(target=self.receive, args=(self.client,))
            self.t.start()
            print('Connected')
 
        return True
 
    def stop(self):
        self.bConnect = False       
        if hasattr(self, 'client'):            
            self.client.close()
            del(self.client)
            print('Client Stop') 
            self.disconn.disconn_signal.emit()
 
    def receive(self, client):
        while self.bConnect:            
            try:
                recv = client.recv(1024)                
            except Exception as e:
                print('Recv() Error :', e)                
                break
            else:
                # file receive
                if str(recv, encoding='utf-8')[0] == 'f':
                    nowdir = os.getcwd()
                    with open(nowdir+"\\recv_"+str(recv, encoding='utf-8').split("/")[1], 'wb') as f:
                        try:
                            data = client.recv(int(str(recv, encoding='utf-8').split("/")[2]))
                            f.write(data)
                        except Exception as ex:
                            print("File receiving error : ", ex)
                # msg receive
                else:                
                    msg = str(recv, encoding='utf-8')
                    if msg:
                        self.recv.recv_signal.emit(msg)
                        print('[RECV]:', msg)
 
        self.stop()
 
    def send(self, msg, isfile):
        if not self.bConnect:
            return

        # file send
        if isfile == True:
            if not exists(msg):
                print("no file in directory")
                return

            filesize = os.path.getsize(os.getcwd()+"//"+msg)
            self.client.send(("f/" + msg + "/" + str(filesize)).encode())
            
            with open(msg, 'rb') as f:
                try:
                    data = b""
                    for line in f:
                        data+= line
                    self.client.send(data)
                except Exception as ex:
                    print("File sending error : ", ex)

        # msg send
        else:
            try:            
                self.client.send(("m" + msg).encode())
            except Exception as e:
                print('Send() Error : ', e)
