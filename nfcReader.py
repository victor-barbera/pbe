#!/usr/bin/env python3
import threading, time
from pynfc import Nfc
import os



class Rfid_reader:
    def __init__(self,NfcDisp) :
            self.n = Nfc(NfcDisp)
        
    # return uid in hexa str 
    def read_uid(self):
        for target in self.n.poll() :
            try:
                id = target.uid
            except:
                pass
            else:  
                return id.decode().upper()
                

if __name__ == "__main__":
    threading.Thread(target=aux).start()
    rf = Rfid_reader("pn532_i2c:/dev/i2c-1")
    rep = 'z'
    while rep!='n':
        _=os.system("clear")
        print(">    Apropa una targeta NFC per llegir-la:")
        uid = rf.read_uid()
        print(">    UID:  " + uid)
        # emulació de do-while amb python
        while True :
            rep = input("\n<    Vols llegir una altra targeta? : [s/n] ")
            if rep=='s' or rep=='n' :
                break
    print("\nPROGRAMA FINALITZAT")
