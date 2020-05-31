import socket
import select
import threading
import sys
from PyQt5.QtWidgets import qApp
from win10toast import ToastNotifier
import time

class ClientSocket():
    def __init__(self, ip, port, data, header_length):
        self.ip = ip
        self.port = port
        self.data = data
        self.header_length = header_length

        # toast notification in windows
        self.toaster  = ToastNotifier()

        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to a given ip and port
        self.client_socket.connect((self.ip, self.port))

        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        self.client_socket.setblocking(1)

        # Prepare username and header and send them
        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username_header = f"{len(self.data.username):<{self.header_length}}".encode('utf-8')
        self.client_socket.send(username_header + self.data.username.encode('utf-8'))

    def receive_socket_data(self):
        while True:
            try:
                # Receive our "header" containing username length, it's size is defined and constant
                username_header = self.client_socket.recv(self.header_length)

                # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                if not len(username_header):
                    print('Connection closed by the server')
                    sys.exit()
                
                # Convert header to int value
                username_length = int(username_header.decode('utf-8').strip())

                # Receive and decode username
                username = self.client_socket.recv(username_length).decode('utf-8')

                # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                message_header = self.client_socket.recv(self.header_length)
                message_length = int(message_header.decode('utf-8').strip())
                self.message = self.client_socket.recv(message_length).decode('utf-8').strip()
                
                if self.message == '!@#$%^&()-+':
                    # such string exists means server responded that to_person is not avaible on the server
                    self.toaster.show_toast("Clip-to-Clip", "{0} is not available".format(self.data.to_person), icon_path=None, duration=2, threaded=True)
                    while self.toaster.notification_active(): time.sleep(0.3)
                else:
                    self.toaster.show_toast("Clip-to-Clip", "Received clip from {0}".format(username), icon_path=None, duration=2, threaded=True)
                    while self.toaster.notification_active(): time.sleep(0.1)
            
            except ConnectionError:
                print('Conncetion closed by server')
                self.toaster.show_toast("Clip-to-Clip", "Server has closed the connection", icon_path=None, duration=2, threaded=True)
                while self.toaster.notification_active(): time.sleep(0.3)
                qApp.quit()
                sys.exit()