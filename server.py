import os, sys
import random
import string
import socket
import json
import threading
from socket import error as SocketError
from time import sleep, time

salaStatus = {}
server_socket = 0
host_ip = ""
conn = 0

def save_json(data: bytes) -> None:
    """Saves json packets to file and name it with id"""
    filename = ''.join(
        random.choice(string.digits)
        for _ in range(3)
    ) + '.json'
    with open(filename, 'wb') as f:
        f.write(data)
    print('saved to', filename)

def conecta_cliente():
    global server_socket
    global host_ip
    global conn
    
    port = 10001  

    server_socket = socket.socket()  

    server_socket.bind((host_ip, port))  

    server_socket.listen(2)
    print("Esperando conexao")
    conn, address = server_socket.accept() 
    print("Connection from: " + str(address))
    
def recebe_status_cliente():
    global server_socket
    global salaStatus
    global conn

    while True:
        sleep(1)
        salaStatus = conn.recv(1024).decode()
        while not salaStatus:
            sleep(1)
            salaStatus = conn.recv(1024).decode()
            break
            if len(salaStatus) == 0:
              print("Servidor distribuído desconectado")
              conn, address = server_socket.accept() 
              print("Connection from: " + str(address))

        print("\n")
        print("Status da sala: " + salaStatus)
        print("\n")
        print("...............MENU..DE..COMANDOS...............")
        print("1 Ligar Lampada 1")
        print("2 Desligar Lampada 1")
        print("3 Ligar Lampada 2")
        print("4 Desligar Lampada 2")
        print("5 Ligar Ar Condicionado")
        print("6 Desligar Ar Condicionado")
        print("7 Ligar Projetor Multimidia")
        print("8 Desligar Projetor Multimidia")
        print("9 Ligar Alarme")
        print("10 Desligar Alarme")
        print("11 Ligar todas as lampadas")
        print("12 Desligar todos os aparelhos")
        print("\n")
        comando = input("Digite uma opcao -> ")
        print("Processando requisicao...")

        try:
          if comando == "1":
            data = '{"L_01": "ON"}'
            conn.send(data.encode())

          elif comando == "2":
            data = '{"L_01": "OFF"}' 
            conn.send(data.encode())

          elif comando == "3":
            data = '{"L_02": "ON"}' 
            conn.send(data.encode())

          elif comando == "4":
            data = '{"L_02": "OFF"}' 
            conn.send(data.encode())

          elif comando == "5":
            data = '{"AC": "ON"}' 
            conn.send(data.encode())

          elif comando == "6":
            data = '{"AC": "OFF"}' 
            conn.send(data.encode())

          elif comando == "7":
            data = '{"PR": "ON"}' 
            conn.send(data.encode())

          elif comando == "8":
            data = '{"PR": "OFF"}' 
            conn.send(data.encode())

          elif comando == "9":
            data = '{"AL_BZ": "ON"}' 
            conn.send(data.encode())

          elif comando == "10":
            data = '{"AL_BZ": "OFF"}' 
            conn.send(data.encode())

          elif comando == "11":
            data = '{"L_ALL": "ON"}' 
            conn.send(data.encode())

          elif comando == "12":
            data = '{"ALL_OFF": "ON"}' 
            conn.send(data.encode())

          else:
            print("Comando invalido")
            data = '{"INVALID_CMD": "1"}' 
            conn.send(data.encode())

        except SocketError as e:
            print("Falha na comunicação com o servidor distribuído. Tentando reconexão...")
            sleep(1)
            conecta_cliente()

    conn.close()  

def main():
  global host_ip

  if(len(sys.argv) != 2):
    print("Argumento inválido.")
    print("Exemplo de uso: python3 server.py 164.41.98.16")
    os._exit(os.EX_OK)

  host_ip = str(sys.argv[1])
  conecta_cliente()
  recebe_status_cliente()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass