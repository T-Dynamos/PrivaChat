import appServer
import _thread
from colorama import *
import os

B = Style.BRIGHT + Fore.BLUE
G = Style.BRIGHT + Fore.GREEN
C = Style.BRIGHT + Fore.CYAN
Y = Style.BRIGHT + Fore.YELLOW
M = Style.BRIGHT + Fore.MAGENTA
W = Style.BRIGHT + Fore.WHITE
R = Style.BRIGHT + Fore.RED
P = Style.BRIGHT + Fore.LIGHTMAGENTA_EX

class CliHandler():
    logs = ["Welcome to PrivaChat!"]
    errors = []
    name = "core"
    connect = None

    def add_logs(self,log):
        self.logs.append(log)

    def add_error(self,error):
        self.errors.append(error)

    def print_log(self,log):
        print(f"{W}[{B}LOGGER{W}] {Y}{log}")

    def print_error(self,error):
        print(f"{W}[{R}ERROR{W}] {P}{error}")

    def start_server(self,port,arg):
        appServer.start_server(port,self.add_logs,self.add_error)

    def print_message(self,message):
        print(f"[{self.name}] {message}")

    def isint(self,string):
        try:
            string = int(string)
            return True
        except Exception:
            return False

    def pass_it(self):
        pass

    def execute_command(self,command):
        if command.startswith("server"):
            if self.isint(command.split(" ")[-1].strip()):
                self._thread = _thread.start_new_thread(self.start_server,(int(command.split(" ")[-1].strip()),""))
                #self.logs.append(f"Sever started on {command.split(' ')[-1].strip()}")
                self.print_log(f"{self.logs[-1]}")
            else:
                self.print_error("Please provide a valid port")

        elif command.strip() == "log":
            self.print_log(f"{self.logs[-1]}")

        elif command.strip() == "logs":
            for log in self.logs:
                self.print_log(f"{log}")

        elif command.startswith("nickname"):
            if command.strip()[-1] == "nickname":
                self.print_log(f"Your current name is '{self.name}'")
            else:
                self.name = command.split(" ")[-1].strip()
                self.print_log(f"Nickname set {self.name}")

        elif command.startswith("connect"):
            if command.strip()[-1] == "connect":
                self.print_log("Please provide a vaild address (eg, 127.0.0.1:9876)")
            else:
                try:
                    self.port = command.split(" ")[-1].strip().split(":")[-1]
                    self.addr = command.split(" ")[-1].strip().split(":")[0]
                except Exception:
                    return self.print_error("Please provide a vaild address (eg, 127.0.0.1:9876)")
                self.connect = appServer.handle_client(self.name,self.pass_it,lambda msg,nickname: print(f"{W}[{P}{nickname}{W}] {msg}"),self.port,self.addr,lambda : print,lambda : print)
                _thread.start_new_thread(self.connect[-1],())
                self.logs.append(f"Connected to {command.split(' ')[-1].strip()}")

        if command == "clients":
            self.print_message(str(appServer.clients))

        elif command.startswith("clear"):
            os.system("clear" if os.name != "nt" else "cls")
        else:
            if self.connect is not None:
                self.connect[0](command)

    def mainloop(self):
        while True:
            try:
                command = input(f"{W}[{Y}{self.name}{W}]>> {G} ")
            except Exception:
                exit("Exit cleanly!")
            self.execute_command(command)

CliHandler().mainloop()
