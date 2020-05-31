from pynput import keyboard
from PyQt5.QtCore import QThread
import clipboard
from clientSocket import ClientSocket
import threading
from win10toast import ToastNotifier
import os

class SystemHandle(QThread):
    def __init__(self, data, parent=None):
        super().__init__(parent)

        self.copy = keyboard.Key.f7
        self.paste = keyboard.Key.f10
        self.file = keyboard.Key.f4

        self.controller = keyboard.Controller()
        self.data = data
        self.socket = ClientSocket('192.168.43.154', 1234, self.data, 10)

    def on_press(self, key):
        '''
        checking which key is pressed

        :param key: key which is pressed by the user
        '''

        if key == self.copy:
            message = clipboard.paste()
            
            message = message.encode('utf-8')
            message_header = f"{len(message):<{10}}".encode('utf-8')
            
            to_person = self.data.to_person.encode('utf-8')
            to_person_header = f"{len(to_person):<{10}}".encode('utf-8')

            if self.data.to_person == '':
                ToastNotifier().show_toast("Clip-to-Clip", "Person name is not defined whom you want to send", icon_path=None, duration=2, threaded=True)
            else:
                self.socket.client_socket.send(message_header + message + to_person_header + to_person)
        
        elif key == self.paste:
            self.controller.type(self.socket.message)

        elif key == self.file:
            if self.data.filename == '':
                ToastNotifier().show_toast("Clip-to-Clip", 'Filename is not defined', icon_path=None, duration=2, threaded=True)
            else:
                with open(os.path.join(self.data.path, self.data.filename), 'a+', newline='') as file:
                    file.write(clipboard.paste() + '\n\n')
                    ToastNotifier().show_toast("Clip-to-Clip", "Data inserted in {0}".format(self.data.filename), icon_path=None, duration=2, threaded=True)

        if key == keyboard.Key.esc:
            return False

    def start_listen(self):
        '''
        creating thread of socket receiving data and keyboard key press
        '''
        receive_thread = threading.Thread(target=self.socket.receive_socket_data)
        receive_thread.start()
        
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

        receive_thread.join()

    def run(self):
        self.start_listen()
