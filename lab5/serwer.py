import socket
from _thread import *
import threading
import hashlib
from typing import List
import time
import json
import re

Slownik_hasel = {}
"""Hasła trzymane są w shadow.txt w postaci hashy"""
#'123123':'96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e' #haslo 123123
#'000001': 'a7fda0b61e2047f0f1057d1f5f064c272fd5d490961c531f4df64b0dd354683a' #haslo 000001

ILOSC_RUND = 10
MIN_UZYTKOWNIKOW = 2
MAX_UZYTKOWNIKOW = 10
NIESKONCZONOSC_POLACZEN = 100
Ilosc_graczy = 0
Slownik_nazwa_klient = {}
Kolejka_graczy = []
Czas_do_rundy = 300 #5*60
Slownik_slow = {}
Slownik_punktow = {}
Slownik_punktow_plik = {}

"""Słownik na hinty"""
Slownik_hint = {
    'a':1,
    'ą':1,
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
    """Rozlaczanie i usuwanie ze slownika uzytkowikow:klientow"""
    try:
        Slownik_nazwa_klient.pop(nazwa)
    except:
        print("Niematakiego usera")
    try:
        client.close()
    except:
        print("połączenie zakończono")


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
        polaczenie.send(str.encode('-\n'))
        return False, nazwa_uzy
    else:
        if nazwa_uzy in Slownik_nazwa_klient: 
            """Zeby nie bylo sytuacji ze ktos sie łączy i gra sam ze sobą nabija sb punkty"""
            polaczenie.send(str.encode('-\n'))
            return False, nazwa_uzy
        else:

            Polacz_ladnie(polaczenie, nazwa_uzy)
            polaczenie.send(str.encode('+\n'))
            return True, nazwa_uzy


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


def Wprowadz_dane(e, client):
    """Sprawdza wprowadzone słowo od klienta"""
    try:
        p = time.time()
        slowo = client.recv(2048)
        slowo = str(slowo.decode())
        slowo = slowo.lower()
        k = time.time() 
        return str(slowo) +":"+ str(k-p)
    except:
        print("blad przy przesylaniu slowa")
        return str("0:11")


def Obsluga_klienta(client, adres):
    """Obsluga_klienta(client) - nowy watek komunikuje sie z klientem"""
    global Ilosc_graczy
    global Kolejka_graczy
    global Slownik_slow
    global Slownik_punktow

    czy_uwierzytelniony, nazwa_uzy = Uwierzytelnienie(client)
    if (czy_uwierzytelniony == False):
        client.close()
    else:
        Kolejka_graczy.append(nazwa_uzy)
        Ilosc_graczy +=1
        Slownik_slow[nazwa_uzy] = ""
        Slownik_punktow[nazwa_uzy] = 0

        while(True):
            if(Slownik_slow[nazwa_uzy] != ""):
                break
            time.sleep(2)
        
        #tego uzywam do zliczania punktow ze slowa
        slowo = Slownik_slow[nazwa_uzy]
        nie_odgadniete_literki = slowo
        #10 rund
        for runda in range(10):
            e = threading.Event()
            t = ThreadWithReturnValue(target=Wprowadz_dane, args=(e,client))
            t.start()
            parse = t.join(10)
            if parse != None:
                #ktos wyslal stringa z wiecej niz jednym znakiem :
                if parse.count(":") > 1:
                    print("Jakis gamoń mi to chce popsuć - rozłączam")
                    try:
                        Slownik_slow.pop(nazwa_uzy)
                        Rozlacz_ladnie(client, nazwa_uzy)
                        return False
                    except:
                        print("błąd w obsłudze klienta - rozlacz ladnie")
                    return False
                parse = parse.split(":")
                wprowadzone_dane, czas = parse[0], parse[1]

            if t.is_alive():
                #jeszcze nie skonczono wpisywania <-> kończe wątek i wyrzucam gracza
                e.set()
                try:
                    #rozlaczam po 10s 
                    Slownik_slow.pop(nazwa_uzy)
                    Rozlacz_ladnie(client, nazwa_uzy)
                    return False
                except:
                    print("błąd w obsłudze klienta - rozlacz ladnie - rozłączony albo słownik wybuchł")
                    return False
            else:
                #skonczono wpisywanie
                if Wprowadz_dane == "0" and czas == "11":
                    #nastąpił błąd w funkcji wprowadzania <-> rozłączam
                    print("blad w funkcji Wprowadz_dane")
                    try:
                        Slownik_slow.pop(nazwa_uzy)
                        Rozlacz_ladnie(client, nazwa_uzy)
                        return False
                    except:
                        print("błąd w obsłudze klienta - rozlacz ladnie - Wprowadz dane - rozłączony albo słownik wybuchł")
                        return False
                        
                if float(czas) > 2:
                    #odpowiedz po 2s
                    try:
                        client.send(str.encode("#\n"))
                        continue
                    except:
                        #klient rozłączony <-> rozłączam go ładnie
                        Slownik_slow.pop(nazwa_uzy)
                        Rozlacz_ladnie(client, nazwa_uzy)
                        return False
                
                if "=" == wprowadzone_dane[0]:
                    #zgadywanie slowa
                    if slowo == wprowadzone_dane[1:]:
                        #slowo zgadniete
                        try:
                            client.send(str.encode("=\n"))
                            Slownik_punktow[nazwa_uzy] += 5
                            client.send(str.encode(str(Slownik_punktow[nazwa_uzy])+"\n"))
                            client.send(str.encode("?\n"))
                            Slownik_slow.pop(nazwa_uzy)
                            Rozlacz_ladnie(client, nazwa_uzy)
                            return True
                        except:
                            print("Jakis blad przy zgadywaniu slowa")
                            try:
                                Slownik_slow.pop(nazwa_uzy)
                                Rozlacz_ladnie(client, nazwa_uzy)
                            except:
                                print("Boze ile bledow")
                            return False
                    else:
                        #niepoprawne słowo
                        try:
                            client.send(str.encode("!\n"))
                            continue
                        except:
                            print("Jakis blad przy zgadywaniu slowa - klient prawdopodobnie rozlaczony")
                            try:
                                Slownik_slow.pop(nazwa_uzy)
                                Rozlacz_ladnie(client, nazwa_uzy)
                            except:
                                print("Boze ile bledow")
                            return False

                elif "+" == wprowadzone_dane[0]:
                    #zgadywanie litery
                    literka = wprowadzone_dane[1]
                    if literka in nie_odgadniete_literki:
                        #literka w slowie znaleziona
                        try:
                            slowo_tymczasowe = slowo #je wysle uzytkownikowi
                            client.send(str.encode("=\n"))
                            time.sleep(0.2)
                            Slownik_punktow[nazwa_uzy] += nie_odgadniete_literki.count(literka)
                            #wyrzucam wszystkie zgadniete literki
                            nie_odgadniete_literki = nie_odgadniete_literki.replace(literka, "")
                            #zamiana na 0/1 ciąg 1-zgadnieta literka reszte rzeczy wyrzucam ze stringa
                            slowo_tymczasowe = slowo_tymczasowe.replace(literka, "1")
                            slowo_tymczasowe = re.sub(re.compile("[a-z2-9ęóąśłżźćń]"), '0', slowo_tymczasowe)
                            #jak klient wysle jakis syf (np.: +_=-!@$@$#%^$%)to jego problem
                            client.send(str.encode(str(slowo_tymczasowe)+"\n"))
                            continue
                        except:
                            print("Klient rozlaczony albo cos nei tak z moim regexem")
                            try:
                                Slownik_slow.pop(nazwa_uzy)
                                Rozlacz_ladnie(client, nazwa_uzy)
                            except:
                                print("Boze ile bledow w literkach")
                            return False
                    else:
                        #brak takiej literki (znaku/cyfry) jak ktos cos nieladnego wpisal w slowie
                        try:
                            client.send(str.encode("!\n"))
                            continue
                        except:
                            print("Jakis blad przy zgadywaniu slowa - klient prawdopodobnie rozlaczony")
                            try:
                                Slownik_slow.pop(nazwa_uzy)
                                Rozlacz_ladnie(client, nazwa_uzy)
                            except:
                                print("Boze ile bledow - brak literki znaku cyfry")
                            return False

                else:
                    #niespodziewana odpowiedz
                    try:
                        client.send(str.encode("?\n"))
                        Slownik_slow.pop(nazwa_uzy)
                        Rozlacz_ladnie(client, nazwa_uzy)
                        return False
                    except:
                        try:
                            Slownik_slow.pop(nazwa_uzy)
                            Rozlacz_ladnie(client, nazwa_uzy)
                        except:
                            print("Boze ile bledow nie moge wyslac ?")
                        print("wprowadzono niezrozumianą sekwencje - dodatkowo błąd z wysyłaniem ?")
                        return False

        #koniec rundy
        
        #Koniec obsługi <-> koniec połączenia klienta wracam do Gry
        Slownik_slow.pop(nazwa_uzy)
        Rozlacz_ladnie(client, nazwa_uzy)
        return True


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
        #rysowanie pasku ładowania do kolejnej gry (jesli zbierze sie odp ilosc graczy)
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
            time.sleep(2) #GRY BEDĄ DZIAŁAŁY ASYNCHRONICZNIE ALE ZEBY NIE BYŁO PROBLEMU Z R/W DO PLIKU
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
        klient.send(str.encode(hint)) #niewiem czy ma byc koniec linii  


def Wez_slownik_punkty():
    """Bierze aktualne wyniki z pliku"""
    global Slownik_punktow_plik
    Slownik_punktow_plik = json.load(open("punkty.txt"))


def Zapis_slownika_punkty():
    """Zapisuje aktualne wyniki do pliku"""
    global Slownik_punktow_plik
    json.dump(Slownik_punktow_plik, open("punkty.txt", 'w'))


def Gra(Bierzaca_gra_gracze, Ilosc_w_grze):
    """dostaje liste 10-2 graczy z kolejki odsługuje wszystkich naraz a później się wyłącza"""
    global Slownik_slow
    global Slownik_punktow
    global Slownik_punktow_plik
    global Slownik_nazwa_klient

    tablica_klientow = []
    for i in range(Ilosc_w_grze):
        tablica_klientow.append(Slownik_nazwa_klient[Bierzaca_gra_gracze[i]])

    #wybieramy wg kolejnosci użytkownika <-> WPROWADZENIE SŁOWA
    for i in range(Ilosc_w_grze):
        try:
            tablica_klientow[0].send(str.encode("@\n"))
            
            e = threading.Event()
            t = ThreadWithReturnValue(target=Wprowadz_slowo, args=(e,tablica_klientow[0]))
            t.start()
            slowo = t.join(2)
            #czekaj 2 sekundy
            
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
    
    hint = Przetlumacz_na_hinta(slowo)
    print("Wybrano słowo: " + hint)
    Broadcast_hinta(tablica_klientow, hint)
    print("Wysłano hint: " + hint)

    #wysyłam klientom slowa gdy beda nie puste rozpocznie sie runda
    for nazwa_uzy in Bierzaca_gra_gracze:
        Slownik_slow[nazwa_uzy] = slowo

    #obsluga 10 rund po stronie klienta
    # Gra staje się zombie czeka 100s na zakończenie gier wszystkich graczy a nastepnie dokonuje operacji zapisu do pliku
    time.sleep(103)
    Wez_slownik_punkty()
    for nazwa_uzy in Bierzaca_gra_gracze: #jeden gracz w jednej grze po jej zakonczeniui tak musi czekac w kolejce 2s
        Wez_slownik_punkty[nazwa_uzy] += Slownik_punktow[nazwa_uzy] 
    #nawet jesli uzytkownik sie rozłączy punkty zostaną dodane
    #aktualizacja slownika dla kazdego gracza w grze <-> zapisuje
    Zapis_slownika_punkty()

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
