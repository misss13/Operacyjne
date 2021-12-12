import socket
from _thread import *
import threading
import hashlib
from typing import List
import time

Slownik_hasel = {
    '123123':'96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e' #haslo 123123
}

MIN_UZYTKOWNIKOW = 2
MAX_UZYTKOWNIKOW = 10
Ilosc_wontkow = 0
Lista_klientow = []
Lista_uzytkownikow = []


ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
host = '127.0.0.1' #IP SERWERA
port = 12345 #PORT
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
ServerSocket.listen(MAX_UZYTKOWNIKOW)


def Czy_w_slowniku(slowo: str):
    """Czy_w_slowniku(str) - zwraca True jesli w slowniku występuje podane słowo"""
    f = open('slowa.txt', 'r')
    if(slowo in f.read()):
        True
    else:
        False

def Rozlacz_ladnie(client):
    """Rozlaczanie i usuwanie z listy bierzacych uzytkowikow"""
    
def Polacz_ladnie(client):
    """Dodawanie bierzacych uzytkowikow i do ich listy"""

def Uwierzytelnienie(polaczenie):
    """Uwierzytelnienie(client) - zajmuje sie logowaniem uzytkownika zwraca +/- do klienta gdzie: '+' True, '-' False """
    try:
        nazwa_uzy = polaczenie.recv(2048)
        nazwa_uzy = str(nazwa_uzy.decode())
    except error:
        print("Uwierzytelnienie -nazwa- blad z decode() albo polaczeniem - zakanczam je")
        return False
    try:
        haslo_uzy = polaczenie.recv(2048)
        haslo_uzy = haslo_uzy.decode()
    except:
        print("Uwierzytelnienie -haslo- blad z decode() albo polaczeniem - zakanczam je")
        return False
    
    haslo_uzy=str(hashlib.sha256(haslo_uzy.encode()).hexdigest())
    
    #TODO funkcja updejtujaca baze danych urzytkownikow z pliku

    if (nazwa_uzy not in Slownik_hasel) or (Slownik_hasel[nazwa_uzy] != haslo_uzy):
        polaczenie.send(str.encode('-'))
        return False
    else:
        if nazwa_uzy in Lista_uzytkownikow: 
            """Zeby nie bylo sytuacji ze ktos sie łączy i gra sam ze sobą nabija sb punkty"""
            polaczenie.send(str.encode('-'))
            return False
        else:
            Lista_uzytkownikow.append(nazwa_uzy)
            polaczenie.send(str.encode('+'))
            return True

def Obsluga_klienta(client, adres):
    """Obsluga_klienta(client) - nowy watek komunikuje sie z klientem"""
    if (Uwierzytelnienie(client) == False):
        client.close()
    else:
        print("Yooo")

    

if __name__=="__main__":
    print("Server up")
    while True:
        client, adres = ServerSocket.accept()
        print (adres[0] + " connected")
        start_new_thread(Obsluga_klienta,(client, adres))
        time.sleep(2)
client.close()
ServerSocket.close()
