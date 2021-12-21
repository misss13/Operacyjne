import random
import time 

lista_slow_do_losowania = []

def Zaladuj_slowa():
    print("Rozpoczynam ładowanie słów do tablicy...")
    with open("slowa.txt") as file:
        while (line := file.readline().rstrip()):
            if len(line) >= 5:
                lista_slow_do_losowania.append(line)
    print("Zakonczono ładowanie słów do tablicy")


def Losuj_slowo():
    if len(lista_slow_do_losowania) <= 1:
        return False
    else:
        return random.choice(lista_slow_do_losowania)


Zaladuj_slowa()
print(Losuj_slowo())

