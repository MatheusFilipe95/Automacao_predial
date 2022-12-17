import load
import socket
from socket import error as SocketError
from time import sleep, time

client_socket = 0

def conecta_server():

    global client_socket

    host = load.ip_servidor_central
    port = 10001  
    global client_socket
    while True:
      try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
        client_socket.connect((host, port)) 
        break
      except SocketError as e:
        print(e)
        print("Falha na conexao, tentando novamente em 5 segundos...")
        sleep(5)
        continue