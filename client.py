import RPi.GPIO as GPIO
import json
import load
import socket_connect
import Adafruit_DHT
import board
from socket import error as SocketError
from typing import Dict, Any
from time import sleep, time
from threading import Thread

alarme = False
contadorPessoas = 0
temperatura_humidade = ""
estadosDaSala = {}

estadosDaSala = {
  "estadoSensorPresenca": 0,
  "estadoSensorJanela": 0,
  "estadoSensorPorta": 0,
  "estadoSensorFumaca": 0,
  "estadoSensorEntradaPessoa": 0,
  "estadoSensorSaidaPessoa": 0,
  "estadoLampada1": 0,
  "estadoLampada2": 0,
  "estadoArCondicionado": 0,
  "estadoProjetor": 0,
  "Temperatura/Humidade": "",
  "numeroPessoas": contadorPessoas,
  "mensagens": []
}

DHT_SENSOR = Adafruit_DHT.DHT22

def salaStatus():
  global contadorPessoas
  global estadosDaSala
  global temperatura_humidade
  humidade, temperatura = Adafruit_DHT.read_retry(DHT_SENSOR, load.GPIO_DHT22)
  temperatura_humidade = "Temperatura={0:0.1f}*C Umidade{1:0.1f}%".format(temperatura, humidade)
  
  estadosDaSala["estadoSensorPresenca"] = GPIO.input(load.SPres)
  estadosDaSala["estadoSensorJanela"] = GPIO.input(load.SJan)
  estadosDaSala["estadoSensorPorta"] = GPIO.input(load.SPor)
  estadosDaSala["estadoSensorFumaca"] = GPIO.input(load.SFum)
  estadosDaSala["estadoSensorEntradaPessoa"] = GPIO.input(load.SC_IN)
  estadosDaSala["estadoSensorSaidaPessoa"] = GPIO.input(load.SC_OUT)
  estadosDaSala["estadoLampada1"] = GPIO.input(load.L_01)
  estadosDaSala["estadoLampada2"] = GPIO.input(load.L_02)
  estadosDaSala["estadoArCondicionado"] = GPIO.input(load.AC)
  estadosDaSala["estadoProjetor"] = GPIO.input(load.PR)
  estadosDaSala["Temperatura/Humidade"] = temperatura_humidade
  estadosDaSala["numeroPessoas"] = contadorPessoas

  return estadosDaSala

def incrementaContador():
  global contadorPessoas
  contadorPessoas += 1

def decrementaContador():
  global contadorPessoas
  if (contadorPessoas > 0 ):
    contadorPessoas -= 1


def envia_msg():
    global estadosDaSala

    message = str(salaStatus())  # take input
    while True:
      try:
        socket_connect.client_socket.send(message.encode())  # send message
        estadosDaSala["mensagens"].clear()
        break
      except SocketError as e:
        print(e)
        sleep(1)
        socket_connect.conecta_server()

def executa_comando():
  global alarme
  global estadosDaSala
  
  while True:
    try:
      data = socket_connect.client_socket.recv(1024).decode()
      break
    except SocketError as e:
      print(e)
      sleep(1)
      continue

  if data:
    dataJson = json.loads(data)
    if ('L_01', 'ON') in dataJson.items():
      GPIO.output(load.L_01, True)
      estadosDaSala["mensagens"].append(" * Lampada 1 ligada *")

    elif ('L_01', 'OFF') in dataJson.items():
      GPIO.output(load.L_01, False)

    elif ('L_02', 'ON') in dataJson.items():
      GPIO.output(load.L_02, True)
      estadosDaSala["mensagens"].append(" * Lampada 2 ligada *")

    elif ('L_02', 'OFF') in dataJson.items():
      GPIO.output(load.L_02, False)

    elif ('AC', 'ON') in dataJson.items():
      GPIO.output(load.AC, True)
      estadosDaSala["mensagens"].append(" * Ar Condicionado ligado *")

    elif ('AC', 'OFF') in dataJson.items():
      GPIO.output(load.AC, False)

    elif ('PR', 'ON') in dataJson.items():
      GPIO.output(load.PR, True)
      estadosDaSala["mensagens"].append(" * Projetor ligado *")


    elif ('PR', 'OFF') in dataJson.items():
      GPIO.output(load.PR, False)

    elif ('AL_BZ', 'ON') in dataJson.items():
      if((GPIO.input(load.SPres) == GPIO.LOW and 
          GPIO.input(load.SJan) == GPIO.LOW and 
          GPIO.input(load.SPor) == GPIO.LOW and 
          GPIO.input(load.AL_BZ) == GPIO.LOW)):
        alarme = True
        estadosDaSala["mensagens"].append(" * Alarme ativado *")
      else:
        estadosDaSala["mensagens"].append(" * Nao foi possivel ativar alarme * ")

    elif ('AL_BZ', 'OFF') in dataJson.items():
      alarme = False
      estadosDaSala["mensagens"].append(" * Alarme desativado * ")
      GPIO.output(load.AL_BZ, False)

    elif ('L_ALL', 'ON') in dataJson.items():
      GPIO.output(load.L_01, True)
      GPIO.output(load.L_02, True)

    elif ('ALL_OFF', 'ON') in dataJson.items():
      GPIO.output(load.L_01, False)
      GPIO.output(load.L_02, False)
      GPIO.output(load.PR, False)
      GPIO.output(load.AC, False)
    
    elif ('INVALID_CMD', '1') in dataJson.items():
      return

def thread_detecta_acionamento():
  global estadosDaSala 

  while True:
    if (GPIO.event_detected(load.SC_IN)):
      incrementaContador()

    if (GPIO.event_detected(load.SC_OUT)):
      decrementaContador()

    if (GPIO.event_detected(load.SFum)):
      estadosDaSala["mensagens"].append(" * Presença de fumaça detectada!! Perigo de incêndio * ")
      GPIO.output(load.AL_BZ, True)

    if (GPIO.event_detected(load.SJan)):
      estadosDaSala["mensagens"].append(" * Janelas abertas * ")

    if (GPIO.event_detected(load.SPor)):
      estadosDaSala["mensagens"].append(" * Porta aberta * ")

    if (GPIO.event_detected(load.SPres)):
      estadosDaSala["mensagens"].append(" * Presença detectada dentro da sala * ")

    salaStatus()
    sleep(0.1)

def detecta_presenca():
  while True:
    if ((GPIO.input(load.SPres) == GPIO.HIGH or GPIO.input(load.SPor) == GPIO.HIGH or GPIO.input(load.SJan) == GPIO.HIGH) and alarme == True):
      GPIO.output(load.AL_BZ, True)
    if GPIO.input(load.SPres) == GPIO.HIGH and alarme == False:
      GPIO.output(load.L_01, True)
      GPIO.output(load.L_02, True)
      sleep(15)
      GPIO.output(load.L_01, False)
      GPIO.output(load.L_02, False)
    sleep(5)

def main() -> None:

  print("Para inicializacao, por favor digite o numero da sala: ")
  print("1 - Configurar sala 1")
  print("2 - Configurar sala 2")
  config = input("Digite o numero da sala: ")
  
  if config == "1":
    load.inicializaPinosSala1()
  if config == "2":
    load.inicializaPinosSala2()

  socket_connect.conecta_server()
  
  t1 = Thread(target = thread_detecta_acionamento)
  t1.setDaemon(True)
  t1.start()

  t2 = Thread(target = detecta_presenca)
  t2.setDaemon(True)
  t2.start()

  while True:
    envia_msg()
    executa_comando()
    
if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass