import appServer
import _thread
from colorama import *
import os
import sys
import time 

B = Style.BRIGHT + Fore.BLUE
G = Style.BRIGHT + Fore.GREEN
C = Style.BRIGHT + Fore.CYAN
Y = Style.BRIGHT + Fore.YELLOW
M = Style.BRIGHT + Fore.MAGENTA
W = Style.BRIGHT + Fore.WHITE
R = Style.BRIGHT + Fore.RED
P = Style.BRIGHT + Fore.LIGHTMAGENTA_EX

logo  = f"""{W}
 _____      _             _____ _           _   
|  __ \    (_)           / ____| |         | |  
| |__) | __ ___   ____ _| |    | |__   __ _| |_ 
|  ___/ '__| \ \ / / _` | |    | '_ \ / _` | __|
| |   | |  | |\ V / (_| | |____| | | | (_| | |_ 
|_|   |_|  |_| \_/ \__,_|\_____|_| |_|\__,_|\__|
{C}A private chat platform!                    v1.0
"""
class CliHandler():
    logs = ["Welcome to PrivaChat!"]
    errors = []
    name = "core"
    connect = None
    executed = False

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
        print(f"{W}[{G}SERVER{W}] {R}{message}")

    def isint(self,string):
        try:
            string = int(string)
            return True
        except Exception:
            return False

    def pass_it(self):
        pass

    def execute_command(self,command):
        if command.startswith("server") and self.executed == False:
            if self.isint(command.split(" ")[-1].strip()):
                self._thread = _thread.start_new_thread(self.start_server,(int(command.split(" ")[-1].strip()),""))
                time.sleep(0.3);self.print_log(f"{self.logs[-1]}")
            else:
                self.print_error("Please provide a valid port")
            self.executed = True

        elif command.strip() == "log" and self.executed == False:
            self.print_log(f"{self.logs[-1]}")
            self.executed = True

        elif command.strip() == "logs" and self.executed == False:
            for log in self.logs:
                self.print_log(f"{log}")
            self.executed = True

        elif command.startswith("nickname") and self.executed == False:
            if command.strip()[-1] == "nickname":
                self.print_log(f"Your current name is '{self.name}'")
            else:
                self.name = command.split(" ")[-1].strip()
                self.print_log(f"Nickname set {self.name}")
            self.executed = True

        elif command == "logo" and self.executed == False:
            print(logo)
            self.executed = True

        elif command.startswith("connect") and self.executed == False:
            if command.strip()[-1] == "connect":
                self.print_log("Please provide a vaild address (eg, 127.0.0.1:9876)")
            else:
                try:
                    self.port = command.split(" ")[-1].strip().split(":")[-1]
                    self.addr = command.split(" ")[-1].strip().split(":")[0]
                except Exception:
                    return self.print_error("Please provide a vaild address (eg, 127.0.0.1:9876)")
                self.connect = appServer.handle_client(self.name,self.pass_it,lambda msg,nickname: sys.stdout.write(f"\r{W}[{P}{nickname.strip()}{W}]>> {msg}\n{W}[{Y}{self.name}{W}]>> {G}"),self.port,self.addr,lambda : print,lambda : print)
                _thread.start_new_thread(self.connect[-1],())
                self.logs.append(f"Connected to {command.split(' ')[-1].strip()}")
            self.executed = True

        if command == "clients":
            self.print_message(str(appServer.nicknames))

        elif command.startswith("clear") and self.executed == False:
            os.system("clear" if os.name != "nt" else "cls")
            self.executed = True

        else:
            if self.connect is not None and self.executed == False:
                self.connect[0](command)
                self.executed = True
            else:
                if self.executed == False:
                    os.system(command)

    def mainloop(self):
        while True:
            try:
                command = input(f"{W}[{Y}{self.name}{W}]>> {G} ")
            except Exception:
                exit("Exit cleanly!")
            self.executed = False
            self.execute_command(command)
print(logo)
CliHandler().mainloop()
