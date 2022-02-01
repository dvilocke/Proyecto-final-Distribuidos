#FRONT
#Programador: Ing  Miguel Angel Ramirez Echeverry
import socket
import threading
import pickle
import os
import time
import random
from ui import menu

PORT = 8000
BUFFER_SIZE = 1024

colors = ["black", "white", "red", "blue"]


class Client(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self, target=self.run)
        self.conn = conn
        self.data = any
        self.end = False
        self.id = any
        self.registration = {
            "username":any,
            "color":any,
            "socket_number":any
        }

    def operation(self, cmd):
        self.conn.sendall(pickle.dumps(cmd))
        return pickle.loads(self.conn.recv(BUFFER_SIZE))

    def send_something(self, something):
        self.conn.sendall(pickle.dumps(something))
        return pickle.loads(self.conn.recv(BUFFER_SIZE))

    def send(self, something):
        self.conn.sendall(pickle.dumps(something))

    def delayed_message(self, msg, t):
        print(msg)
        time.sleep(t)

    def throw_dice(self):
        while True:
            os.system("cls")
            print("Your Turn")
            option = int(input('\npress 1 to roll the dice:'))
            if option == 1:
                dice_result =  random.randint(1,6)
                break
        return dice_result

    def play(self):
        while True:
            os.system("cls")
            self.data = pickle.loads(self.conn.recv(BUFFER_SIZE))
            self.delayed_message(msg=self.data, t=5)
            break

        os.system("cls")
        while True:
            self.data = pickle.loads(self.conn.recv(BUFFER_SIZE))
            if self.data == True:
                result = self.throw_dice()
                self.delayed_message(msg=f"\nthe result of the dice is:{result}", t=4)
                self.send(something=result)
                os.system("cls")
            else:
                print(self.data)


    def waiting_room(self):
        while True:
            os.system("cls")
            self.data = pickle.loads(self.conn.recv(BUFFER_SIZE))

            while True:
                os.system("cls")
                print(self.data, end="\n-------------------------------------")
                option = int(input('\npress 1 to roll the dice:'))
                if option == 1:
                    dice_result =  random.randint(1,6)
                    self.delayed_message(msg=f"\nthe result of the dice is:{dice_result}", t=4)
                    break
            self.send(something= [self.id, dice_result])
            break
        
        self.play()

    def run(self):
        with self.conn:
            while not self.end:
                os.system("cls")
                print(menu(), end="")
                option_user = int(input())
                if option_user == 1:
                    if self.operation(cmd="quantity") < 2:
                        os.system("cls")
                        color = input("choose a color(black, white, red, blue):").lower()
                        if color in colors:
                            if color not in self.operation(cmd="get_colors"):
                                self.registration["username"] = input("Enter Username:")
                                self.registration["color"] = color
                                self.id = self.operation(cmd="get_id")
                                self.registration["socket_number"] = self.id
                                if self.operation(cmd="register"):
                                    if self.send_something(something=self.registration):
                                        self.waiting_room()
                            else:
                                self.delayed_message(msg="that color has already been chosen by another user", t=5)
                        else:
                            self.delayed_message(msg="error, color does not exist", t=5)
                    else:
                        self.delayed_message(msg="server full", t=3)

                elif option_user == 2:
                    if self.operation(cmd="exit"):
                        self.end = True
                else:
                    pass
        print('disconnected')


if __name__ == '__main__':
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((socket.gethostname(), PORT))
    client = Client(conn=my_socket)
    client.start()