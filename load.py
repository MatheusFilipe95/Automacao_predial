import RPi.GPIO as GPIO
from backports import configparser

ip_servidor_central = ""
L01 = 0
L_02 = 0
AC = 0 
PR = 0
AL_BZ = 0

SPres = 0
SFum = 0
SJan = 0
SPor = 0
SC_IN = 0
SC_OUT = 0
GPIO_DHT22 = 0
inputs = []
outputs = []

DHT_SENSOR = 0

def inicializaPinosSala2():

  global ip_servidor_central
  global L_01
  global L_02
  global AC
  global PR
  global AL_BZ

  global SPres
  global SFum
  global SJan
  global SPor
  global SC_IN
  global SC_OUT
  global GPIO_DHT22  
  global inputs
  global outputs

  config = configparser.ConfigParser()
  config.read("configuracao02.ini")

  ip_servidor_central = config.get("sala2config", "ip_servidor_central")
  L_01 = int(config.get("sala2config", "L_01"))
  L_02 = int(config.get("sala2config", "L_02"))
  AC = int(config.get("sala2config", "AC"))
  PR = int(config.get("sala2config", "PR"))
  AL_BZ = int(config.get("sala2config", "AL_BZ"))

  SPres = int(config.get("sala2config", "SPres"))
  SFum = int(config.get("sala2config", "SFum"))
  SJan = int(config.get("sala2config", "SJan"))
  SPor = int(config.get("sala2config", "SPor"))
  SC_IN = int(config.get("sala2config", "SC_IN"))
  SC_OUT = int(config.get("sala2config", "SC_OUT"))
  GPIO_DHT22 = int(config.get("sala2config", "GPIO_DHT22"))

  inputs = [SPres, SFum, SJan, SPor, SC_IN, SC_OUT, GPIO_DHT22]
  outputs = [L_01, L_02, AC, PR, AL_BZ]

  configuraPinos()

def inicializaPinosSala1():

  global ip_servidor_central
  global L_01
  global L_02
  global AC
  global PR
  global AL_BZ

  global SPres
  global SFum
  global SJan
  global SPor
  global SC_IN
  global SC_OUT
  global GPIO_DHT22  
  global inputs
  global outputs

  config = configparser.ConfigParser()
  config.read("configuracao01.ini")

  ip_servidor_central = config.get("sala1config", "ip_servidor_central")
  L_01 = int(config.get("sala1config", "L_01"))
  L_02 = int(config.get("sala1config", "L_02"))
  AC = int(config.get("sala1config", "AC"))
  PR = int(config.get("sala1config", "PR"))
  AL_BZ = int(config.get("sala1config", "AL_BZ"))

  SPres = int(config.get("sala1config", "SPres"))
  SFum = int(config.get("sala1config", "SFum"))
  SJan = int(config.get("sala1config", "SJan"))
  SPor = int(config.get("sala1config", "SPor"))
  SC_IN = int(config.get("sala1config", "SC_IN"))
  SC_OUT = int(config.get("sala1config", "SC_OUT"))
  GPIO_DHT22 = int(config.get("sala1config", "GPIO_DHT22"))

  inputs = [SPres, SFum, SJan, SPor, SC_IN, SC_OUT, GPIO_DHT22]
  outputs = [L_01, L_02, AC, PR, AL_BZ]
  
  configuraPinos()

def configuraPinos():
  global SPres
  global SFum
  global SJan
  global SPor
  global SC_IN
  global SC_OUT
  global DHT_SENSOR
  global inputs
  global outputs

  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  #Configuracao dos Pinos como Entradas / Saidas

  GPIO.setup(inputs, GPIO.IN)
  GPIO.setup(outputs, GPIO.OUT)

  GPIO.output(AL_BZ, False)

  # Configura deteccao de acao do Botao
  GPIO.add_event_detect(SPres, GPIO.RISING)
  GPIO.add_event_detect(SFum, GPIO.RISING)
  GPIO.add_event_detect(SJan, GPIO.RISING)
  GPIO.add_event_detect(SPor, GPIO.RISING)
  GPIO.add_event_detect(SC_IN, GPIO.RISING)
  GPIO.add_event_detect(SC_OUT, GPIO.RISING)
