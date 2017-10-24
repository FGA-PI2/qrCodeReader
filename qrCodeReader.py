#!/usr/bin/python
from sys import argv
import zbar
import json
import requests


API_URL = 'http://dev-pi2-api.herokuapp.com/'
quantity = 0
# create a Processor
proc = zbar.Processor()

# configure the Processor
proc.parse_config('enable')

# initialize the Processor using the default webcam
device = '/dev/video1'
if len(argv) > 1:
    device = argv[1]
proc.init(device)

# setup a callback

def update(url,data):
    headers = {'X-HTTP-Method-Override':'PATCH'}
    request = requests.put(url,data=data, headers=headers)

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


        bebidas_list = list()
        for item,index in zip(result[0]['pedido'],len(result[0]['pedido'])):

            bebida[index] = (
                requests.get(API_URL+"bebida/{}".format(item['bebida'])).content,
                item
            )

            if bebida[index]['remaining_quantity'] < item['volume']:
                print("Não há {} o suficiente para fazer esta bebida. Entre em contato com o Administrador").format(bebida[index]['nome'])
                enough_bebida = False

            else:
                enough_bebida = True


        #SEND ALL DATAS TO ELETRONIC HERE
        if enough_bebida is True:

            list_of_orders = list()

            for item in result[0]['pedido']:

                drink_to_make = {
                    'posicao' : item['bebida']['posicao'],
                    'volume' : item['volume']
                }

                #Essa lista é o que eletronica deve ler para realizar o pedido
                list_of_orders.append(drink_to_make)



            result[0]["qr_code"]["is_valid"] = False
            url = API_URL+"code/{}/".format(result[0]["qr_code"]["id"])

            qrcode = {
                "is_valid": False,
                "qr_code": result[0]["qr_code"]["qr_code"],
                "usuario": result[0]["qr_code"]["usuario"]
            }

            update_qr_code_status = update(url,qrcode)

            for bebida in bebidas_list:
                subtract_volume_of_drink = update(API_URL+"bebida/{}/".format(bebida[0]['nome']),{"remaining_quantity":bebida[1]['nome']})

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
