import time

def szukacz1():
    f = open('slowa.txt', 'r')
    lines = f.read()
    answer = lines.find('oiiiiiii')
    print(answer)

def szukacz2():
    file = open('slowa.txt', 'r')
    search_word = "oiiiiii"
    if(search_word in file.read()):
        print("word found")
    else:
        print("word not found")

if __name__=="__main__":
    """suma1=0
    suma2=0
    for i in range(100):
        s1 = time.time()
        szukacz1()
        k1 = time.time()
        s2 = time.time()
        szukacz2()
        k2 = time.time()
        suma1 = (k1-s1)
        suma2 = (k2-s2)
    print(suma1/100)
    print(suma2/100)"""
    szukacz1()
    szukacz2()

"""
    0.003072795867919922
    0.0030373668670654295
"""
""" 
    0.003118598461151123
    0.0030711746215820314 -> szukacz2 file.read() szybszy
"""