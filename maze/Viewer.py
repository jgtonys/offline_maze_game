import os

def main_view(_str):
    strlen = 78 - len(_str)
    print("-"*79)
    print(_str)
    print("{:>76}".format("Made by JG"))
    print("-"*79+"\n")

def main_select():
    print("1. Login")
    print("2. Register")
    print("3. Quit")
    print("4. Feedback Time")
    print("\n")
    ch = input("Input : ")
    os.system("cls")
    return ch


def menu_view(user,_str):
    print("-"*79)
    print(_str)
    print("{:>76}".format("Made by JG"))
    print(str(user.username) + "님의 LV:"+str(user.level)+" Coin:"+str(user.coin)+"개")
    print("-"*79+"\n")


def menu_select():
    print("1. Start Maze")
    print("2. Ranking")
    print("3. Coin Shop")
    print("4. My Inventory")
    print("0. Back")
    print("\n")
    ch = input("input : ")
    os.system("cls")
    return ch
