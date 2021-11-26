# import pycom
from network import LoRa, Bluetooth
import socket
import time
import machine
import struct
import ubinascii
from my_lora_secret import my_app_eui
from my_lora_secret import my_app_key

#blu = Bluetooth()
devs_arr = []
#number = 256
#bytestring = number.to_bytes(2, 'big')
#bytestring2 = 
#print("integer {int} in bytes is {bytes}".format(int=number, bytes=bytestring))

# Send only one byte by default unless we need more
bytes_len = 0x00
# Encode type to be sent -- TYPE_PULSE1 = 0x0A; //2bytes relative pulse count
decode_type = 0x0A
# Initialise LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, device_class=LoRa.CLASS_A)
# create an OTAA authentication parameters, change them to the
# provided credentials
app_eui = ubinascii.unhexlify(my_app_eui)
app_key = ubinascii.unhexlify(my_app_key)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
# wait until the module has joined the network

while True:
    #lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    while not lora.has_joined():
        time.sleep(2)
        print('Not yet joined...')
    print('Joined LoRaWAN')
    blu = Bluetooth()
    # blu = Bluetooth(antenna=Bluetooth.EXT_ANT)
    blu.start_scan(10)
    while blu.isscanning():
        adv = blu.get_adv()
        if adv:
            if adv[0] not in devs_arr:
                devs_arr.append(adv[0])
    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    # send some data
    devs_arr_len = len(devs_arr)
    #if devs_arr_len > 0:
    #    if devs_arr_len > 255:
    #        devs_arr_len -= 255
    #        bytes_len = 0x01
        
    #s.send(bytes([decode_type, bytestring]))
    #s.send(struct.pack(">H", number))
    #print(struct.pack(">H", number))
    #s.send(bytes([decode_type, bytes(bytestring)]))
    #s.send(decode_type, bytestring)
    #s.send(bytes([decode_type, bytes_len, devs_arr_len]))
    s.send(struct.pack('!bH', decode_type, devs_arr_len))
    print("Bluetooth-Devices: ",devs_arr_len)
    #print(devs_arr)
    for i in devs_arr:
        print(i)
    del devs_arr[:]
    #print(bytes_arr)
    #devs_arr = []
    #bytes_len = 0x00
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)
    # get any data received (if any...)
    data = s.recv(64)
    if data:
        print(data)
    # Sleep
    print("Going to sleep mode... ")
    #print("Going to sleep mode... " + str(time.ticks_ms()))
    time.sleep(600)
    #machine.sleep(36000, False)
    #print("Waking up... "+ str(time.ticks_ms()))
