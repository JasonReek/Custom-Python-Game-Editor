import os 
import threading 

game_thread = None
class GameWindowThread(threading.Thread):
    def __init__(self, name):
        super(GameWindowThread, self).__init__()
        self.name = name 

    def run(self):
        os.system("python GameWindow.py")

def isGameRunning():
    for thread in threading.enumerate():
        if thread.name == "GameThread":
            return True
    return False  