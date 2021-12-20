import socket
from _thread import *
import threading
import hashlib
from typing import List, Type
import time
import re

a = [''] * 5
print(a)
def funkcja():
    while True:
        print("yoo")
        a = input()
        if a == "a":
            return True
bb = funkcja()
a="alohaaoiiii"
print(a.count("a"))
a = a.replace("a","1")
a = a.replace(" ", "")
print(re.sub(re.compile("[a-zA-Z2-9]"), '0', a))
#print(a.replace(re.compile("[a-zA-Z2-9]"), "0", string))


def Wprowadz_dane(e, cos):
    """Sprawdza wprowadzone słowo od klienta"""
    try:
        p = time.time()
        #print(time.time())
        slowo = input()
        slowo = slowo.lower()
        k = time.time()
        return slowo +":"+str(k-p)
    except:
        print("blad przy przesylaniu slowa")
        return "1:1"


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

e = threading.Event()
t = ThreadWithReturnValue(target=Wprowadz_dane, args=(e, "10"))
t.start()
wprowadzone_dane, czas = "", 10
parse = t.join(6)
if parse != None:
    parse = parse.split(":")
    wprowadzone_dane, czas = parse[0], parse[1]
if t.is_alive():
    #jeszcze nie skonczono wpisywania <-> kończe wątek i wyrzucam gracza
    e.set()
    try:
        print("minelo 6s")
    except:
        print("błąd w obsłudze klienta - rozłączony albo słownik wybuchł")
else:
    #skonczono wpisywanie
    print(type(wprowadzone_dane))
    print(float(czas))

