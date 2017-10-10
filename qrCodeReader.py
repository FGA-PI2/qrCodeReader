#!/usr/bin/python
from sys import argv
import zbar
import json
import requests

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
def my_handler(proc, image, closure):  
    
    #for symbol in image.symbols:
    for symbol in image:
        # do something useful with results

		# convert the symbol.data (aka the data extracted from the qr code)	to the string format	
        qrCodeAsString = '"%s"' % symbol.data
        print qrCodeAsString
        # deletes the first the " punctuation so we can load the text string as JSON data
        qrCodeAsString = qrCodeAsString[1:len(qrCodeAsString)-1]
        # converts to JSON data
        qrCodeAsJSON = json.loads(qrCodeAsString)

        # prints and validates the data 
        #print "QR Code: %s" % qrCodeAsJSON
        print "Usuario da compra (QR Code): %s" % qrCodeAsJSON["usuario"]
        print "Data de compra (QR Code): %s" % qrCodeAsJSON["data_compra"]
        print "--------------------"

        # checks with the data from compra's API

        id = 20
        responseFromAPI = requests.get("https://pi2-api.herokuapp.com/compra/%s" % id)

        apiDataAsJson = responseFromAPI.json()

        print "Usuario da compra (API): %s" % apiDataAsJson["usuario"]
        print "Data de compra (API): %s" % apiDataAsJson["data_compra"]
        print "Is valid? (API): " + str(apiDataAsJson["qr_code"]["is_valid"])
        print "--------------------"

        if (qrCodeAsJSON["data_compra"] == apiDataAsJson["data_compra"]) and (qrCodeAsJSON["usuario"] == apiDataAsJson["usuario"]) and (apiDataAsJson["qr_code"]["is_valid"]):
        	print "Informacoes da compra bateram, validar os dados do is_valid"
        else:
        	print "Dados nao bateram, esse QR Code nao e valido"



        #print "User ID: %s" % qrCodeAsJSON["usuario"]
        #print "JSON Bebida: %s" % qrCodeAsJSON["pedido"][0]
        #print "Bebida 1: %s" % qrCodeAsJSON["pedido"][0]["bebida"]
        #print "Porcentagem Bebida 1: %s " % qrCodeAsJSON["pedido"][0]["porcentagem"]
        #print "Bebida 2: %s" % qrCodeAsJSON["pedido"][1]["bebida"]
        #print "Porcentagem Bebida 2: %s " % qrCodeAsJSON["pedido"][1]["porcentagem"]
        #if qrCodeAsJSON["gelo"]:
       # 	print "Gelo: Sim"
        #else:
        #	print "Gelo: Nao"
        #print "Tamanho do copo: %s ml" % qrCodeAsJSON["tamanho"]  
        
        #print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
#        if symbol.data == "teste.org":
#        	print "teste 1"
#        if symbol.data == "http://teste2.org":
#        	print "teste 2"
#        else:
#        	print "nao ta dando"

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