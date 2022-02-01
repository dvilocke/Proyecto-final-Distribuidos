#BACKEND
#Programador: Ing Miguel Angel Ramirez Echeverry
import socket
import threading
import pickle
import time
from ui import player_information, results_message, update

PORT = 8000
BUFFER_SIZE = 1024

bd = {"user":[], "socket":[], "colors":[], "dice":[]}
        
flag_1 = False
flag_2 = False

counter = 0



#shift control variables
finish_game = False
user_id = 0

class User:
    def __init__(self, username, color, socket_number, connected=False) -> None:
        self.username = username
        self.color = color
        self.socket_number = socket_number
        self.connected = connected
        self.dice = any
        self.turn = False

    def __str__(self) -> str:
        return f"username:{self.username}, color:{self.color}, socket_number:{self.socket_number}, dice:{self.dice}"

    def __repr__(self) -> str:
        return f"<username:{self.username}, color:{self.color}, socket_number:{self.socket_number}, dice:{self.dice}>"


class Server(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self, target=self.run)
        self.conn = conn
        self.addr = addr
        self.data = any
        self.register = False
        self.end = False
        #ID -> controla los indice correspondientes de la BD
        self.id = any

    def send_something(self, something):
        self.conn.sendall(pickle.dumps(something))

    def commands(self, cmd):
        if cmd == "exit":
            #metodo Put
            self.end = True
            self.send_something(something=True)

        elif cmd == "quantity":
            self.send_something(something=len(bd["user"]))

        elif cmd == "get_colors":
            self.send_something(something=bd["colors"])

        elif cmd == "get_id":
            self.send_something(something=len(bd["socket"]))

        elif cmd == "register":
            #metodo Put
            self.register = True
            self.send_something(something=True)

    def shift_system(self):
        global user_id, contador
        while not finish_game:
            user = bd["user"][user_id]
            socket = bd["socket"][user.socket_number]

            if socket == self.conn:
                #procceso
                self.conn.sendall(pickle.dumps(True))
                self.data = pickle.loads(self.conn.recv(BUFFER_SIZE))
                if self.data:
                    user.dice = self.data

                    for s in bd["socket"]:
                        if s != self.conn:
                            s.sendall(pickle.dumps(update(user=user)))
                    
                    time.sleep(6)

                    if user_id == 0:
                        user_id = 1
                    else:
                        user_id = 0


    def play(self):
        #we must synchronize them
        while True:
            if flag_1 and flag_2:
                #arrancar primero, problema de sincronizacion --- OJO
                self.send_something(something=results_message(bd=bd["user"]))
                
                self.shift_system()

    def organize_players(self):
        #print(bd["user"])
        bd["user"] = sorted(bd["user"], key=lambda x: x.dice)[::-1]
        #print(bd["user"])

    def waiting_room(self):
        while True:
            if len(bd["user"]) == 2:
                self.send_something(something= player_information(bd=bd["user"]))
                self.data = pickle.loads(self.conn.recv(BUFFER_SIZE))
                self.id = self.data[0]
                bd["user"][self.id].dice = self.data[1]
                bd["dice"].append({self.id:self.data[1]})
                if len(bd["dice"]) == 1:
                    global flag_1
                    #I send one player to play, the other organizes the players, in the play function they must be synchronized
                    flag_1 = True
                    self.play()
                    break
                else:
                    global flag_2
                    self.organize_players()
                    flag_2 = True
                    self.play()
                    break

    def run(self):
        with self.conn:
            print(self.addr)
            while not self.end:
                if not self.register:
                    self.data = pickle.loads(self.conn.recv(BUFFER_SIZE))
                    self.commands(self.data)

                elif self.register:
                    self.data = pickle.loads(self.conn.recv(BUFFER_SIZE))
                    user = User(username=self.data["username"], color=self.data["color"], socket_number=self.data["socket_number"], connected=True)
                    bd["user"].append(user)
                    bd["colors"].append(user.color)
                    bd["socket"].append(self.conn)
                    self.send_something(something=True)
                    self.waiting_room()


        print(f'User:{self.addr} disconnected')


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((socket.gethostname(), PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            Server(conn, addr).start()