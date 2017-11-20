import sqlite3 as sql
import os
import DBcon,Viewer,GameController,Rank,Shop

flag = 0

class User():
    def __init__(self,username,password,level,coin,character,elapsed_time):
        self.username = username
        self.password = password
        self.level = level
        self.coin = coin
        self.elapsed_time = elapsed_time
        self.character = character
    def update(self,db_row):
        self.username = db_row[0][0]
        self.password = db_row[0][1]
        self.level = db_row[0][2]
        self.coin = db_row[0][3]
        self.character = db_row[0][4]
        self.elapsed_time = db_row[0][5]
    def shopping(self,character,coin):
        self.character = character
        self.coin = coin



def login():
    global flag
    flag = 0
    user = user_info()
    while flag is 0:
        status(user)
        user.update(login_refresh(user.username))

def register():
    msg = ""
    while True:
        Viewer.main_view("MAZE Registering")
        print("주의! 한글로 만들면 2자이하, 영어로 만들면 13자 이하입니다.")
        print(msg)
        _id = input("ID: ")
        _pw = input("PW: ")
        m = DBcon.valid_id_check(_id,_pw)
        if len(_id) == 0: msg = "INVALID ID!"
        elif m != 2: msg = "USED ID!"
        else:
            DBcon.db_register(_id,_pw)
            os.system("cls")
            print("Registered Successfully!")
            break
        os.system("cls")

def status(user):
    global flag
    while True:
        Viewer.menu_view(user,"MAZE")
        ch = Viewer.menu_select()
        if ch == '1':
            GameController.start_maze(user)
            break
        elif ch == '2':ranking()
        elif ch == '3':shop(user)
        elif ch == '4':inventory(user)
        elif ch == '0':flag = 1; break
        else: print("INVALID INPUT")


def inventory(user):
    l = DBcon.showinventory(user)
    Viewer.menu_view(user,"MAZE Inventory")
    print("당신이 가지고 있는 스킨들\n")
    for i in range(len(l)):
        print(str(l[i][0])+"번 스킨: "+l[i][1],end="")
    ch = input("\n스킨을 바꾸시겠습니까? (y/n): ")
    if ch == 'y':
        c = input("몇번 스킨으로 바꾸시겠습니다? :")
        DBcon.skinchange(user,int(c))
        user.update(login_refresh(user.username))
    os.system("cls")

def user_info():
    msg = ""
    while True:
        Viewer.main_view("MAZE LOGIN")
        print(msg)
        username = input("ID를 입력하세요 : ")
        password = input("PW를 입력하세요 : ")
        m = DBcon.valid_id_check(username,password)
        if m == 2: msg = "INVALID ID!"
        elif m == 3: msg = "PASSWORD INCORRECT!"
        else: os.system("cls");break
        os.system("cls")
    user = User(m[0][0],m[0][1],m[0][2],m[0][3],m[0][4],m[0][5])
    return user

def login_refresh(username):
    return DBcon.db_refresh(username)

def ranking():
    Rank.get_ranking()

def shop(user):
    Viewer.main_view("MAZE COIN SHOP")
    ch = Shop.purchase(user)
    if ch == 'cancel': return 0
    else:
        os.system("cls")
        Viewer.main_view("MAZE Coin Shop")
        print("성공적으로 구매하였습니다.")
        input("계속하려면 아무키나 누르세요")
        os.system("cls")
        
