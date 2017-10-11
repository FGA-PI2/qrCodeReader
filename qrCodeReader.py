#!/usr/bin/python
from sys import argv
import zbar
import json
import requests
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

def processQRCode(qrcode):
    ++quantity
    print("RECEBI OS TREM PARCEIRO!")
    print "Usuario da compra (QR Code): %s" % qrcode["usuario"]
    print "Data de compra (QR Code): %s" % qrcode["data_compra"]
    print "--------------------"

    # checks with the data from compra's API

    data = qrcode["data_compra"]
    user = qrcode["usuario"]
    responseFromAPI = requests.get("http://dev-pi2-api.herokuapp.com/compra/?data_compra=%s&usuario__id=%s" %(data, user))

    result  = json.loads(responseFromAPI.content)
    print result[0]

    if (result[0]["qr_code"]["is_valid"] == True):
        print ("QR Code Valido!")
        print ("O pedido %s sera feito!" %result[0]["nome"])
        print (result[0]["qr_code"]["is_valid"])
        #SEND ALL DATAS TO ELETRONIC HERE
        result[0]["qr_code"]["is_valid"] = False
        r = requests.patch("http://dev-pi2-api.herokuapp.com/compra/?data_compra=%s&usuario__id=%s" %(data, user), data=result[0])

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
        qrCodeAsString = '"%s"' % symbol.data
        print qrCodeAsString
        # deletes the first the " punctuation so we can load the text string as JSON data
        qrCodeAsString = qrCodeAsString[1:len(qrCodeAsString)-1]
        # converts to JSON data
        qrCodeAsJSON = json.loads(qrCodeAsString)

        processQRCode(qrCodeAsJSON)
       

        # print "Usuario da compra (API): %s" % result[0]["usuario"]
        # print "Data de compra (API): %s" % result["data_compra"]
        # print "Is valid? (API): " + str(result["qr_code"]["is_valid"])
        # print "--------------------"



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