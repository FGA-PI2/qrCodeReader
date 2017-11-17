#!/usr/bin/python

from sys import argv
import zbar
import json
import requests
import operator
from teste import serialuc32

API_URL = 'http://dev-pi2-api.herokuapp.com/'
quantity = 0
# create a Processor
proc = zbar.Processor()

# configure the Processor
proc.parse_config('enable')

# initialize the Processor using the default webcam
device = '/dev/video0'
if len(argv) > 1:
    device = argv[1]
proc.init(device)

# setup a callback

def update(url,data,request_type="put"):

    if request_type is "put":
        headers = {'X-HTTP-Method-Override':'PATCH'}
        request = requests.put(url,data=data, headers=headers)
    else:
        headers = {'X-HTTP-Method-Override':'PATCH'}
        request = requests.patch(url,data=data, headers=headers)


    return request

def processQRCode(qrcode):
    ++quantity
    print("RECEBI OS TREM PARCEIRO!")
    print "Usuario da compra (QR Code): {}".format(qrcode["usuario"])
    print "Data de compra (QR Code): {}".format(qrcode["data_compra"])
    print "--------------------"

    # checks with the data from compra's API

    data = qrcode["data_compra"]
    user = qrcode["usuario"]
    responseFromAPI = requests.get(API_URL+"compra/?data_compra={}&usuario__id={}".format(data, user))

    result  = json.loads(responseFromAPI.content)

    if (result[0]["qr_code"]["is_valid"] == True):


        bebida = list()
        bebida = list()
        for item,index in zip(result[0]['pedido'],range(0,len(result[0]['pedido'])) ):

            enough_bebida = list()

            tupla = (json.loads(requests.get(API_URL+"bebida/{}".format(item['bebida']['nome'])).content),item)

            bebida.append(tupla)
            

            print(bebida[index][0]['remaining_quantity'],item['volume'])  
            if bebida[index][0]['remaining_quantity'] < item['volume']:
                print("Nao ha {} o suficiente para fazer esta bebida. Entre em contato com o Administrador").format(bebida[index][0]['nome'])
                enough_bebida.append(False)

            else:
                print('volume suficiente')
                enough_bebida.append(True)


        #SEND ALL DATAS TO ELETRONIC HERE
        if False not in enough_bebida:

            list_of_orders = list()

            drinks = {}


            drinks = {

                    1 : 0,
                    2 : 0,
                    3 : 0
            }

            for item in result[0]['pedido']:

                drink_to_make = {
                    'posicao' : item['bebida']['posicao'],
                    'volume' : item['volume']
                }

                drinks[drink_to_make['posicao']] = drink_to_make['volume']  
            
                



                #Essa lista e o que eletronica deve ler para realizar o pedido
                #list_of_orders.append(drink_to_make["posicao"],drink_to_make['volume']) 
                



            result[0]["qr_code"]["is_valid"] = False
            url = API_URL+"code/{}/".format(result[0]["qr_code"]["id"])

            qrcode = {
                "is_valid": False,
                "qr_code": result[0]["qr_code"]["qr_code"],
                "usuario": result[0]["qr_code"]["usuario"]
            }

            update_qr_code_status = update(url,qrcode)
            print(update_qr_code_status)

            for item in bebida:
                print(item)
                volume_restante = item[0]['remaining_quantity'] - item[1]['volume']
                print(volume_restante,"{}".format(item[0]['nome']))
                subtract_volume_of_drink = update(API_URL+"bebida/{}/".format(item[0]['nome']),{"remaining_quantity":volume_restante},"patch")
                print(subtract_volume_of_drink.request)

                      
                    

            string = ""    
            for i in drinks.values():
                string = string+str(i)+" "
       
            if(result[0]["gelo"] == True):
                string = string + "1"
            else:
                string = string + "0"


            #sorted_x = sorted(drinks.items(), key=operator.itemgetter(0))
            print(drinks.keys())
            print(string)
            serialuc32(string)

    else:
        print ("QR Code Invalido!")
        print ("Este pedido ja foi retirado!")
        print (result[0]["qr_code"]["is_valid"])

def my_handler(proc, image, closure):

    #for symbol in image.symbols:
    for symbol in image:
        # do something useful with results
        print "OI"
		# convert the symbol.data (aka the data extracted from the qr code)	to the string format
        qrCodeAsString = '"{}"'.format(symbol.data)
        print qrCodeAsString
        # deletes the first the " punctuation so we can load the text string as JSON data
        qrCodeAsString = qrCodeAsString[1:len(qrCodeAsString)-1]
        # converts to JSON data
        qrCodeAsJSON = json.loads(qrCodeAsString)

        processQRCode(qrCodeAsJSON)


proc.set_data_handler(my_handler)

# enable the preview window
proc.visible = True

# initiate scanning
proc.active = True
try:
    # keep scanning until user provides key/mouse input
    proc.user_wait()
except zbar.WindowClosed, e:
    pass
