import lcd_henok
import time
import RPi.GPIO as GPIO
import threading
try:
    from Tkinter import *
except ImportError:
    from tkinter import *

return_item = False
return_item_t = False
return_item_q = False


buttonPin = 17
inp = ""
last_inp = ""
product_barcodes_names = [['0009458800010419', 'CLAMOX', 10.50],
                          ['6251001210415','FINE TISSUE', 5.0],
                          ['3387390334470', 'NESQUIK', 2.0],
                          ['6291001000029', 'MASAFI WATER', 1.0],
                          ['Product1', 'PEPSI 300ML', 1.5],
                          ['Product2', 'ALMARI MILK 0.5L', 3.0],
                          ['Product4', 'DORITOS CHIPS', 2.0],
                          ['Product3', 'AL-MARI YOGURT', 5.0]]

items_purchased = []

items_purchased_quantity = []

total = 0.0
first_time_price = True
first_time_quantity = True
first_time_total = True
first_time_purchase = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def executeButtonThread():
   while(1):
       if(buttonPressed()):
           global return_item
           global return_item_t
           return_item = True
           return_item_t = True
           time.sleep(1/10)
       else:
            time.sleep(1/10)

       
def buttonPressed():
    if(GPIO.input(buttonPin)):
        return(False)
    else:
        return(True)    


def keydown(e):
    global inp
    inp = inp + str(e.char)
def getProductName(barcode):
    for i in range(len(product_barcodes_names)):
        if(product_barcodes_names[i][0] == barcode):
            (product_barcodes_names[i][1])
            return(product_barcodes_names[i][1])

def getProductPrice(barcode):
    for i in range(len(product_barcodes_names)):
        if(product_barcodes_names[i][0] == barcode):
            return(str(product_barcodes_names[i][2]))


def displayAtTheEnd(msg, line_number):
    length = len(str(msg))
    lcd_henok.lcd_display(msg, line_number, 16-length)
    time.sleep(1.0/10000.0)

def updatePriceOnLcd():
    global last_inp
    price = float(getProductPrice(last_inp))
    global return_item
    global total        
    global first_time_prices
    
    if(first_time_price):
        lcd_henok.lcd_display('PRICE        ', 3, 0)
        displayAtTheEnd(str(price), 3)
        time.sleep(1.0/10000.0)
        first_time = False
        return_item = False
    else:
        displayAtTheEnd(str(price), 3)
        time.sleep(1.0/10000.0)
        return_item = False

def updateQuantityOnLcd():
    global first_time_quantity
    global items_purchased
    global items_purchased_quantity
    global last_inp
    if(first_time_quantity):
        lcd_henok.lcd_display('QUANTITY        ', 2, 0)
        ind = items_purchased.index(last_inp)
        displayAtTheEnd(str(items_purchased_quantity[ind]), 2)
        time.sleep(1.0/10000.0)
        first_time_quantity = False
    else:
        displayAtTheEnd("      ", 2)
        ind = items_purchased.index(last_inp)
        time.sleep(1.0/10000.0)
        displayAtTheEnd(str(items_purchased_quantity[ind]), 2)
        first_time_quantity = False
def notPurchasedLcdUpdate():
    lcd_henok.clear_all()
    lcd_henok.lcd_display('Unpercased Item', 1, 0)
    first_time_quantity = True
    
def updateTotalOnLcd():
    global last_inp
    global first_time_total
    global return_item_t
    if(first_time_total):
        lcd_henok.lcd_display('TOTAL        ', 4, 0)
        displayAtTheEnd(total, 4)
        time.sleep(1.0/10000.0)
        first_time = False
    else:
        displayAtTheEnd(total, 4)
        time.sleep(1.0/10000.0)
        
def updateLcd():
    global inp
    global items_purchased
    global last_inp
    lcd_henok.lcd_clear_line(1)
    time.sleep(1.0/1000.0)
    lcd_henok.lcd_display(getProductName(last_inp), 1, 0)
    #lcd_henok.lcd_clear_line(2)
    time.sleep(1.0/10000.0)
    global total
    global return_item_t
    if(return_item_t):
        total = total - float(getProductPrice(last_inp))
        return_item_t = False
        
    else:
        total = total + float(getProductPrice(last_inp))
    updatePriceOnLcd()
    updateQuantityOnLcd()
    updateTotalOnLcd()


def itemPurchased():
    global first_time_purchase
    global items_purchased
    global inp
    global last_inp
    global items_purchased_quantity
    global return_item_q
    if(first_time_purchase):
        items_purchased.append(last_inp)
        items_purchased_quantity.append(1)
        first_time_purchase = False
    elif(return_item_q):
        if(last_inp in items_purchased):
            ind = items_purchased.index(last_inp)
            items_purchased_quantity[ind] = items_purchased_quantity[ind] - 1
        else:
            items_purchased.append(last_inp)
            items_purchased_quantity.append(1)
        return_item_q = False
    else:
        if(last_inp in items_purchased):
            ind = items_purchased.index(last_inp)
            items_purchased_quantity[ind] = items_purchased_quantity[ind] + 1
        else:
            items_purchased.append(last_inp)
            items_purchased_quantity.append(1)
            
def returnItemChecker():
    global items_purchased_quantity
    global total
    if(last_inp in items_purchased):
        print("Can return")
        ind = items_purchased.index(last_inp)
        items_purchased_quantity[ind] = items_purchased_quantity[ind] - 1
        if(items_purchased_quantity[ind] >= 0.0):
            lcd_henok.lcd_clear_line(1)
            time.sleep(1.0/10000.0)
            lcd_henok.lcd_display(getProductName(last_inp), 1, 0)
            time.sleep(1.0/10000.0)
            displayAtTheEnd("      ", 2)
            displayAtTheEnd(items_purchased_quantity[ind], 2)
            price = -1*float(getProductPrice(last_inp))
            displayAtTheEnd("      ", 3)
            time.sleep(1.0/10000.0)
            displayAtTheEnd(str(price), 3)
            total = total + price
            displayAtTheEnd("      ", 4)
            time.sleep(1.0/10000.0)
            displayAtTheEnd(str(total), 4)
        else:
            print("-ve")
            notPurchasedLcdUpdate()
        
    else:
        print('dont  return')
        notPurchasedLcdUpdate()

    
def returnKey(e):
    global return_item
    global return_item_t
    global last_inp
    global inp
    last_inp = inp
    inp = ""
    if(first_time_purchase and return_item):
        notPurchasedLcdUpdate()
        return_item = False
        return_item_t = False
    elif(return_item):
        print('trying to return')
        returnItemChecker()
        return_item = False
        return_item_t = False
    else:
        itemPurchased()
        print(items_purchased)
        print(items_purchased_quantity)
        updateLcd()
    
root = Tk()
root.title("Command Center")
buttonThread = threading.Thread(target=executeButtonThread)

    
root.bind("<KeyPress>", keydown)
root.bind("<Return>", returnKey)
buttonThread.start()
mainloop()
root.mainloop()
