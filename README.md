
# Trabalho 01 - Automação Predial

## Aluno
|Matrícula | Aluno |
| -- | -- |
| 140155350  |  Matheus Filipe Faria Alves de Andrade |

## Objetivo
Este trabalho tem por objetivo a criação de um sistema distribuído de automação predial para monitoramento e acionamento de sensores e dispositivos de um prédio com múltiplas salas. O sistema deve ser desenvolvido para funcionar em um conjunto de placas Raspberry Pi com um servidor central responsável pelo controle e interface com o usuário e servidores distribuídos para leitura e acionamento dos dispositivos. Dentre os dispositivos envolvidos estão o monitoramento de temperatura e umidade, sensores de presença, sensores de fumaça, sensores de contagem de pessoas, sensores de abertura e fechamento de portas e janelas, acionamento de lâmpadas, aparelhos de ar-condicionado, alarme e aspersores de água em caso de incêndio.

## Instruções para execução

### 1) Clone o repositório:
```sh 
git clone <link>
```

### 2) Acesse a pasta do projeto:
```sh 
cd Projeto_1
```

**Obs:** Substituir <nome_de_usuario> pelo seu nome de usuário dentro da placa nos comandos abaixo.

Para executar o projeto precisaremos de dois terminais, um para o servidor central e o outro para o servidor distribuído.

No terminal do servidor central:

#### 1) Copiar a pasta para dentro da rhaspberry:
```sh
scp -P 13508 -r ./Projeto_1 <nome_de_usuario>@164.41.98.16:~
cd Projeto1
```

### 2) Instalar as dependências do projeto:
```sh
pip3 install Adafruit_DHT 
pip3 install adafruit-blinka
pip3 install configparser
```

### 3) Executar o programa:
```sh
python3 server.py 164.41.98.16
```

No terminal do servidor distribuído:

#### 1) Copiar a pasta para dentro da rhaspberry:
```sh
scp -P 13508 -r ./Projeto_1 <nome_de_usuario>@164.41.98.26:~
cd Projeto1
```

### 2) Instalar as dependências do projeto:
```sh
pip3 install Adafruit_DHT 
pip3 install adafruit-blinka
pip3 install configparser
```

### 3) Executar o programa:
```sh
python3 client.py
```

