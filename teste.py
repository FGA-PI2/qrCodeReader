import serial #biblioteca para utilizar serial
import time 
import sys
import RPi.GPIO as GPIO # uso de portas GPIO
import requests #request realizado para jason
import Adafruit_DHT #biblioteca para usar sensor DHT 
import thread
GPIO.setmode(GPIO.BCM) #padrao de pinagem BCM
# Define o tipo de sensor
sensor = Adafruit_DHT.DHT22 #tipo de sensor de temperatura utilizado 

GPIO.setup(23,GPIO.IN) #setando como pino de entrada
GPIO.setup(17,GPIO.IN)
GPIO.setup(24, GPIO.OUT)
# Define a GPIO conectada ao pino de dados do sensor
pino_sensor = 25 #pino de dados sensor de temperatura
pino_rele = 24

def requerido():
    r=requests.get("http://pi2-api.herokuapp.com/compra")
    var= r.json();
    return var[0]['id']#mudar 0 pelo numero do id recebido na rasp


def ler_temperatura(fase): #ler temperatura pino(25)
    while(1):
        # Efetua a leitura do sensor
        umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor)
        # Caso leitura esteja ok, mostra os valores na tela
        if temp is not None:
            if temp > 1.5:
                GPIO.output(pino_rele,GPIO.HIGH)  
            else:
                GPIO.output(pino_rele,GPIO.LOW)
        else:
            # Mensagem de erro de comunicacao com o sensor
            print("Falha ao ler dados do DHT11 !!!")
        time.sleep(5)
        

def serialuc32(comando):
    print("recebi parceiro")
    comunicacaoserial = serial.Serial('/dev/ttyUSB1',9600,timeout=80000)
    time.sleep(3) #tempo necessario para manter uma conexao de dados segura.

    #comando="a"
    comunicacaoserial.write(comando)#mensagem a ser enviada
    print("enviado")
    dado = comunicacaoserial.readline()
    print("recebido...")
    print(comando)
        
    comunicacaoserial.close()

#try:
#    
#    #thread.start_new_thread(serialuc32,("a",))
#    thread.start_new_thread(ler_temperatura,(fase,))
#except Exception, e:
#    print ("Erro: pala na thread",e)
#
#while 1:
#    if GPIO.input(23):
#        print("seguranca violada")
#    time.sleep(2)
#while 1:
#   pass
