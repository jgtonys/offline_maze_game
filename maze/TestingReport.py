import os

def report():
    l = open(r'beta.txt','r')
    while True:
        r = l.readline()
        if r == "":break
        print(r,end="")
    l.close()
    input()
    os.system("cls")
