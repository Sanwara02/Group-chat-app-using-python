import socket
import threading 
import tkinter 
import tkinter.scrolledtext
from tkinter import simpledialog 
from tkinter import* 

host='127.0.0.1'                                                           #ip address for client and server must b same on local devices
port=9090

class Client:
    def __init__(self, host, port):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))                                     #.connect is used to make a connection between server side and client side

        msg=tkinter.Tk()                                                   #creating a window which will ask for username of client
        msg.withdraw() 
        self.username=simpledialog.askstring("SERVER BASED CHAT ROOM", "Please choose a username", parent=msg)
        
        self.finish= False     
        self.running= True

        thread1= threading.Thread(target=self.loop)                         #multi threading
        thread2= threading.Thread(target=self.receive)

        thread1.start()
        thread2.start()

    def loop(self): 

        self.win=tkinter.Tk()
        self.win.configure(bg="lavender")

        self.label = tkinter.Label(self.win, text="Your Conversations:", bg="lavender")
        self.label.config(font=("Serif",12))
        self.label.pack(padx=20, pady=5)


        self.chat_field=tkinter.scrolledtext.ScrolledText(self.win)                                 #creating chat log window
        self.win.title("LETS CHAT")                                                                 #title
        self.chat_field.pack(padx=10, pady=5)
        self.chat_field.config(state='disabled')

        self.msg_back = tkinter.Label(self.win, text="Type your message:", bg="lavender")           #title of input window
        self.msg_back.config(font=("Serif",12))
        self.msg_back.pack(padx=20, pady=5)

        self.input= tkinter.Text(self.win, height=3)                                                 #input window
        self.input.pack(padx=10, pady=5)

        self.send_button= tkinter.Button(self.win, text="Send", command=self.write)                  #creating send button
        self.send_button.config(font=("Serif",12))
        self.send_button.pack(padx=10, pady=5)

        self.finish=True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)                                              #closing window after exit button is pressed
        self.win.mainloop()

    def write(self):
        message=f"{self.username}: {self.input.get('1.0', 'end')}"                                    #'1.0','end' specifies that complete message will be sent right from beginning
        self.sock.send(message.encode('utf-8'))                                                       #can use ascii as well in place of utf-8
        self.input.delete('1.0','end')                                                                #to clear the input text field after each message is sent

    def stop(self):
        self.running= False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message=self.sock.recv(1024).decode('utf-8')                                          #1024: buff size; maximum length of a message
                if message=='USER':
                    self.sock.send(self.username.encode('utf-8'))

                else:
                    if self.finish:
                        self.chat_field.config(state='normal')                                        #if this state is changed to disables, no messages can be sent
                        self.chat_field.insert('end', message)
                        self.chat_field.yview('end')
                        self.chat_field.config(state='disabled')                                      #if this state is changed, previously sent messages can be manipulated by any client which is undesirable

            except ConnectionAbortedError:                                                            #printing error only if server is disconnected
                break

            except:
                print('Error')                                                                        #for any ohter kind of error
                break

client=Client(host,port)