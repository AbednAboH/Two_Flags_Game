import socket
import sys
import threading

import tkinter as tk

def Send(connection,client_address):
    while True:
        data = str(input())
        if data:

            if data[:1] == "r":
                break
            data = bytes(data, "utf-8")
            connection.sendto(data, client_address)
            print('sent data to the client')

def Rec(connection,client_address):
    while True:
        recover = connection.recv(1000)
        print('-----------------------------')
        print('received "%s"' % recover)
        print('-----------------------------')


def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SERVER:
        server_address = ('127.0.0.1', 65432)
        print('starting up on %s port %s' % server_address)
        SERVER.bind(server_address)
        SERVER.listen(1)

        while True:
            print('waiting for connection')
            connection, client_address = SERVER.accept()
            connection.sendto(b'Connected with client!', client_address)
            k = threading.Thread(target=Send, args=(connection,client_address))
            s = threading.Thread(target=Rec, args=(connection,client_address))

            try:
                print('connection from', client_address)
                k.start()
                s.start()
                # Receive the data in small chunks and retransmit it
                # while True:
                #
                #         recover = connection.recv(1000)
                #
                #         print('-----------------------------')
                #         print('received "%s"' % recover)
                #         print('-----------------------------')
                #
                #     data = str(input())
                #
                #     if data:
                #
                #         if data[:1]=="r":
                #             break
                #         data = bytes(data, "utf-8")
                #         connection.sendto(data, client_address)
                #         print('sent data to the client')
            finally:
                # Clean up the connection

                k.join()
                s.join()
                connection.close()


if __name__ == "__main__":
    root = tk.Tk()

    canvas1 = tk.Canvas(root, width=300, height=300)
    canvas1.pack()


    def hello():
        label1 = tk.Label(root, text='Hello World!', fg='green', font=('helvetica', 12, 'bold'))
        canvas1.create_window(150, 200, window=label1)


    button1 = tk.Button(text='start client', command=server, bg='brown', fg='white')
    canvas1.create_window(150, 150, window=button1)

    root.mainloop()
