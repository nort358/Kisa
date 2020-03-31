import socket
import threading
import os
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('', 53210))
serv_sock.listen(1)
connections=list()
thr=list()
chanels=list()
def MAIN():
    i=0
    global LOG
    LOG=open("LOGS.txt",'a+')
    while True:
        client_sock, client_addr = serv_sock.accept()
        print(i+1)
        connections.append(connection(client_sock, client_addr))
        thr.append(threading.Thread(target=connections[i].work))
        thr[i].daemon = True
        thr[i].start()
        #connections[i].work()
        i=i+1


"""def end():
    LOG.close()
    for i in thr:
        i."""

class chanel():
    def __init__(self,name):
        self.name=name
        self.users=list()
        self.work=True
        self.thrs=list()
        print("CREATED")
    def add(self,sock,adress):
        
        def wait(s):
            rez=str(s.recv(1024))
            rez=rez[2:-1]
            if rez=="LEFTCHANNEL":
                return None
            else:
                self.send(":"+rez)
                return 1
        def work(s):
            while True:
                a=wait(s)
                if not a: break
        self.users.append(sock)        
        self.thrs.append(threading.Thread(target=work(sock)))
        print(self.users)
    def send(self,data):
        for user in self.users:
            print (user)
            user.sendall(bytes(data,'utf-8'))

                
        




class connection:
    def __init__(self,client_sock, client_addr):
        self.login=None
        self.channel=None
        self.sock=client_sock
        self.addr=client_addr
        self.inchannel=False
        print('Connected by', self.addr)
    def get(self):#
        rez=str(self.sock.recv(1024))
        rez=rez[2:-1]
        self.save(rez,True)
        return rez
    def send(self,data):#
        self.save(data,False)
        self.sock.sendall(bytes(data,'utf-8'))
    def log(self):#
        self.send("Write Your LOGIN")
        login=self.get()
        self.send("Write Your PASSWORD")
        pwrd=self.get()
        f=open("LP.txt",'r')
        i=0
        r=False
        for line in f:
            if i%2==0:
                if line==login+"\n":
                    r=True
            elif r==True:
                if line==pwrd+"\n":
                    self.login=login
                    f.close()
                    self.send("HI,"+login)
                    return None
                else: break
            i=i+1
        self.send("LOGIN or PASSWOPD is INCORRECT")                  
        f.close()
    def unlogin(self):#
        self.send("Bye,"+self.login)
        self.login=None
    def createchannel(self):
        self.send("Write NAME of channel")
        name=self.get()
        if os.path.exists(name+'.txt'):
           self.send("This NAME is already taken")
           return
        else:
            file=open(name+".txt",'a+')
        self.send("Write PASSWORD of channel")
        pwrd=self.get()
        file.write(pwrd+'\n')
        self.send("CHANNEL "+name+" is CREATED")
        
    def connectchannel(self):
        self.send("Write NAME of channel")
        name=self.get()
        if os.path.exists(name+'.txt'):
            self.send("WELCONE in "+name)
            for ch in chanels:
                if name==ch.name:
                    ch.add(self.sock,self.addr)
                    break
            else:
                chanels.append(chanel(name))
                chanels[-1].add(self.sock,self.addr)
            
        else:
            self.send("WRONG NAME")
    def command(self,data):#Bad work
        if data=="HELP":
            self.help()
        elif data=="CREATEUSER":
            self.createuser()
        elif data=="CREATECHANNEL":
            self.createchannel()
        elif data=="CONNECTCHANNEL":
            self.connectchannel()
        elif data=="LOGIN":
            self.log()
        elif data=="UNLOGIN":
            self.unlogin()
        elif data=="EXIT":
            self.help()
        else:
            self.send("PROBLEMS")        
    def createuser(self):#
        login=None
        pwrd=None
        self.send("Write Your LOGIN")
        login=self.get()
        self.send("Write Your PASSWORD")
        pwrd=self.get()
        f=open("LP.txt",'r')
        i=0
        for line in f:
            if i%2==0:
                if line==login:
                    self.send("THIS NAME IS ALREADY TAKEN")
                    return None
            i=i+1
        f.close()
        f=open("LP.txt",'a')
        f.write(login+"\n")
        f.write(pwrd+"\n")
        f.close()
        self.login=login
        self.send("WELCOME,"+login)
    def save(self,data,g):
        ge="GET:"
        if g==False:
            ge="SEND:"
        LOG.write(ge+data+"\n")
    def help(self):#
        self.send("COMMANDS:HELP,CREATEUSER,CONNECTCHANNEL,LEFTCHANNEL,LOGIN,UNLOGIN,HISTORY,EXIT")
    def work(self):#
        print("start work")
        while True:
            data=self.get()
            if data:
                #self.save(data)
                self.command(data)
                
            else :break
        self.send("End connection")
        self.sock.close()
        print("End connetction with",self.addr)
    
#
#
#
#
#
MAIN()
