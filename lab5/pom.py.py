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
NIESKONCZONOSC_POLACZEN = 100
Ilosc_graczy = 0
Slownik_nazwa_klient = {}
Kolejka_graczy = []
Czas_do_rundy = 300 #5*60

"""Słownik na hinty"""
Slownik_hint = {
    'ą':2,
    'b':3,
    'c':1,
    'ć':1,
    'd':3,
    'e':1,
    'ę':1,
    'f':4,
    'g':3,
    'h':2,
    'i':1,
    'j':2,
    'k':3,
    'l':3,
    'ł':3,
    'm':1,
    'n':1,
    'ń':1,
    'o':1,
    'ó':1,
    'p':2,
    'r':1,
    's':1,
    'ś':1,
    't':3,
    'u':1,
    'w':1,
    'y':2,
    'z':1,
    'ź':1,
    'ż':1
}

ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
host = '127.0.0.1' #IP SERWERA
port = 12345 #PORT
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
ServerSocket.listen(NIESKONCZONOSC_POLACZEN)


class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return



def Update_Slownik_hasel():
    global Slownik_hasel
    Slownik_hasel = json.load(open("shadow.txt"))


def Czy_w_slowniku(slowo: str):
    """Czy_w_slowniku(str) - zwraca True jesli w slowniku występuje podane słowo w przeciwnym wypadku"""
    file = open('slowa.txt', 'r')
    if(slowo in file.read()):
        return True
    else:
        return False


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
    global Kolejka_graczy

    czy_uwierzytelniony, nazwa_uzy = Uwierzytelnienie(client)
    if (czy_uwierzytelniony == False):
        client.close()
    else:
        Kolejka_graczy.append(nazwa_uzy)
        Ilosc_graczy +=1

        time.sleep(1000)
        #Koniec połączenia
        Rozlacz_ladnie(client, nazwa_uzy)


def Rozlacz_reszte(Tablica_klientow, Bierzaca_gra_gracze):
    """Po zakonczeniu gry rozlaczam pozostałych klientow"""
    b = len(Bierzaca_gra_gracze)
    for i in range(b):
        Rozlacz_ladnie(Tablica_klientow[0], Bierzaca_gra_gracze[0])
        Tablica_klientow.remove(Tablica_klientow[0])
        Bierzaca_gra_gracze.remove(Bierzaca_gra_gracze[0])


def Rozlacz_jednego(tablica_klientow, Bierzaca_gra_gracze):
    """Rozłączam jednego klienta w kolejce w bierzącej grze pierwszego"""
    Rozlacz_ladnie(tablica_klientow[0], Bierzaca_gra_gracze[0])
    tablica_klientow.remove(tablica_klientow[0])
    Bierzaca_gra_gracze.remove(Bierzaca_gra_gracze[0])


def Czasomierz():
    """Oblicza czas między rundami oraz sprawdza ilosc graczy w kolejce - jeśli 10 rozpoczyna gre albo czas"""
    global Ilosc_graczy
    global Kolejka_graczy
    global Czas_do_rundy
    global MAX_UZYTKOWNIKOW
    global MIN_UZYTKOWNIKOW

    print("|################|")
    i=0
    ile_razy_kratka = 1
    trwanie_do_rundy = Czas_do_rundy / 2

    while True:
        if i%10 == 0:
            print("|" + "#"*ile_razy_kratka + (16-ile_razy_kratka)*" " + "|")
            ile_razy_kratka += 1

        if (Ilosc_graczy >= MAX_UZYTKOWNIKOW) or (i>=trwanie_do_rundy):
            i=0
            ile_razy_kratka=1
            if(Ilosc_graczy <= MIN_UZYTKOWNIKOW-1):
                continue
            print("Nowa runda")
            Bierzaca_gra_gracze = []
            liczba_graczy = min(Ilosc_graczy, MAX_UZYTKOWNIKOW)
            for j in range(liczba_graczy):
                gracz = Kolejka_graczy.pop(0)
                Bierzaca_gra_gracze.append(gracz)
            Ilosc_graczy -= MAX_UZYTKOWNIKOW
            start_new_thread(Gra,(Bierzaca_gra_gracze, liczba_graczy))
        time.sleep(2)
        i += 1


def Przetlumacz_na_hinta(slowo: str):
    """Zamienia słowo na postać cyfrową tak jak podano w poleceniu z urzyciem słownika"""
    hint = ""
    for i in slowo:
        hint += str(Slownik_hint[i])
    return hint

def Broadcast_hinta(tablica_klientow, hint: str):
    """Wysyłanie do wszystkich wiadomości z hasłem"""
    for klient in tablica_klientow:
        klient.send(str.encode(hint))        

def Wprowadz_slowo(e, client):
    """Sprawdza wprowadzone słowo od klienta"""
    try:
        slowo = client.recv(2048)
        slowo = str(slowo.decode())
        slowo = slowo.lower() 
        return slowo
    except:
        print("blad przy przesylaniu slowa")
        return ""


def Gra(Bierzaca_gra_gracze, Ilosc_w_grze):
    """dostaje liste 10-2 graczy z kolejki"""
    tablica_klientow = []
    for i in range(Ilosc_w_grze):
        tablica_klientow.append(Slownik_nazwa_klient[Bierzaca_gra_gracze[i]])

    #wybieramy wg kolejnosci użytkownika <-> WPROWADZENIE SŁOWA
    for i in range(Ilosc_w_grze):
        try:
            tablica_klientow[0].send(str.encode("@"))
            
            e = threading.Event()
            t = ThreadWithReturnValue(target=Wprowadz_slowo, args=(e,tablica_klientow[0]))
            t.start()
            slowo = t.join(6)
            #czekaj 6 sekund
            
            if t.is_alive():
                #jeszcze nie skonczono wpisywania <-> kończe wątek i wyrzucam gracza
                e.set()
                Rozlacz_jednego(tablica_klientow, Bierzaca_gra_gracze)
                Ilosc_w_grze -= 1
                if Ilosc_w_grze <= 1: # W grze nie może być jeden gracz
                    print("W grze jeden gracz - rozłączam")
                    Rozlacz_reszte(tablica_klientow, Bierzaca_gra_gracze)
                    return False
                continue
            else:
                #skonczono wpisywanie
                if (slowo == "") or (Czy_w_slowniku(slowo) == False):
                    #puste slowo albo brak w słowniku <-> wyrzucam gracza
                    Rozlacz_jednego(tablica_klientow, Bierzaca_gra_gracze)
                    Ilosc_w_grze -= 1
                    if Ilosc_w_grze <= 1:
                        Rozlacz_reszte(tablica_klientow, Bierzaca_gra_gracze)
                        print("W grze jeden gracz - rozłączam")
                        return False
                    continue
                else:
                    #usuwam użytkownika ktory zna słowo
                    print("Wybrano slowo: %s" %(slowo))
                    Rozlacz_jednego(tablica_klientow, Bierzaca_gra_gracze)
                    Ilosc_w_grze -= 1
                    if Ilosc_w_grze <= 0:
                        print("W grze brak graczy - rozłączam")
                        Rozlacz_reszte(tablica_klientow, Bierzaca_gra_gracze)
                        return False
            break
        except:
            #nie ustalono słowa jeden gracz w grze <-> zabijam grę
            print("błąd połączenia - rozłączam")
            Rozlacz_jednego(tablica_klientow, Bierzaca_gra_gracze)
            Ilosc_w_grze -= 1
            if Ilosc_w_grze <= 1:
                print("W grze jeden gracz - rozłączam")
                Rozlacz_reszte(tablica_klientow, Bierzaca_gra_gracze)
                return False
            continue
    
    print("Yooooo dziala")
    #obsluga 10 rund
    hint = Przetlumacz_na_hinta(slowo)
    print(hint)
    Broadcast_hinta(tablica_klientow, hint)

    
if __name__=="__main__":
    print("Server up")
    start_new_thread(Czasomierz,())
    while True:
        client, adres = ServerSocket.accept()
        print (adres[0] + " connected")
        start_new_thread(Obsluga_klienta,(client, adres))
        time.sleep(2)
client.close()
ServerSocket.close()
