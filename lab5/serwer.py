import socket
from _thread import *
import threading
import hashlib
from typing import List
import time
import json

Slownik_hasel = {}
"""Hasła trzymane są w shadow.txt w postaci hashy"""
#'123123':'96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e' #haslo 123123
#'000001': 'a7fda0b61e2047f0f1057d1f5f064c272fd5d490961c531f4df64b0dd354683a' #haslo 000001

MIN_UZYTKOWNIKOW = 2
MAX_UZYTKOWNIKOW = 10
Ilosc_graczy = 0
Slownik_nazwa_klient = {}
Kolejka_graczy = []
Czas_do_rundy = 300 #5*60


ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
host = '127.0.0.1' #IP SERWERA
port = 12345 #PORT
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
ServerSocket.listen(MAX_UZYTKOWNIKOW)

def Update_Slownik_hasel():
    global Slownik_hasel
    Slownik_hasel = json.load(open("shadow.txt"))

def Czy_w_slowniku(slowo: str):
    """Czy_w_slowniku(str) - zwraca True jesli w slowniku występuje podane słowo"""
    f = open('slowa.txt', 'r')
    if(slowo in f.read()):
        True
    else:
        False

def Rozlacz_ladnie(client, nazwa):
    """Rozlaczanie i usuwanie z listy bierzacych uzytkowikow"""
    Slownik_nazwa_klient.pop(nazwa)
    client.close()


def Polacz_ladnie(client, nazwa):
    """Dodawanie bierzacych uzytkowikow do ich listy"""
    Slownik_nazwa_klient[nazwa]=client


def Uwierzytelnienie(polaczenie):
    """Uwierzytelnienie(client) - zajmuje sie logowaniem uzytkownika zwraca +/- do klienta gdzie: '+' True, '-' False """
    try:
        nazwa_uzy = polaczenie.recv(2048)
        nazwa_uzy = str(nazwa_uzy.decode())
    except error:
        print("Uwierzytelnienie -nazwa- blad z decode() albo polaczeniem - zakanczam je")
        return False, "none"
    try:
        haslo_uzy = polaczenie.recv(2048)
        haslo_uzy = haslo_uzy.decode()
    except:
        print("Uwierzytelnienie -haslo- blad z decode() albo polaczeniem - zakanczam je")
        return False, nazwa_uzy
    
    haslo_uzy=str(hashlib.sha256(haslo_uzy.encode()).hexdigest())

    Update_Slownik_hasel()
    #funkcja updejtujaca baze danych urzytkownikow z pliku

    if (nazwa_uzy not in Slownik_hasel) or (Slownik_hasel[nazwa_uzy] != haslo_uzy):
        polaczenie.send(str.encode('-'))
        return False, nazwa_uzy
    else:
        if nazwa_uzy in Slownik_nazwa_klient: 
            """Zeby nie bylo sytuacji ze ktos sie łączy i gra sam ze sobą nabija sb punkty"""
            polaczenie.send(str.encode('-'))
            return False, nazwa_uzy
        else:

            Polacz_ladnie(polaczenie, nazwa_uzy)
            polaczenie.send(str.encode('+'))
            return True, nazwa_uzy


def Obsluga_klienta(client, adres):
    """Obsluga_klienta(client) - nowy watek komunikuje sie z klientem"""
    global Ilosc_graczy
    Ilosc_graczy +=1
    czy_uwierzytelniony, nazwa_uzy = Uwierzytelnienie(client)
    if (czy_uwierzytelniony == False):
        client.close()
    else:
        global Kolejka_graczy
        Kolejka_graczy.append(nazwa_uzy)
        #dodanie gracza do kolejki

        
        a = client.recv(2048)
        a = a.decode()
        print(a)
        time.sleep(100)
        Rozlacz_ladnie(client, nazwa_uzy)

def Czasomierz():
     """Oblicza czas między rundami oraz sprawdza ilosc graczy w kolejce - jeśli 10 rozpoczyna gre"""

def Gra():
    """dostaje liste 10 graczy z kolejki"""

if __name__=="__main__":
    print("Server up")
    while True:
        client, adres = ServerSocket.accept()
        print (adres[0] + " connected")
        start_new_thread(Obsluga_klienta,(client, adres))
        time.sleep(2)
client.close()
ServerSocket.close()
