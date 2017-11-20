import os,Viewer,DBcon

def purchase(user):
    while True:
        print("현재 코인: "+str(user.coin)+"개\n\n")
        li = item_list()
        item,text = li[0],li[1]
        ch = input("\n0. Back\n\n당신의 선택은? : ")
        if ch == '0': os.system("cls");return "cancel"
        else:
            if item[int(ch)] > user.coin:
                os.system("cls")
                Viewer.main_view("MAZE Coin Shop")
                input("코인이 부족합니다.")
            else:
                c = user.coin-item[int(ch)]
                user.shopping(int(ch),c)
                DBcon.db_shopping(user,text[int(ch)])
                return ch

def item_list():
    l = open('src/ch/item_list.txt','r')
    item = [0]
    text = [0]
    li = []
    while True:
        r = l.readline()
        f = r.find("코인")
        k = r.find("개")
        p = r.find("=")
        if f!=-1 and k!=-1:
            item.append(int(r[f+3:k]))
            text.append(r[p+2:])
        if r == "": break
        print(r,end="")
    l.close()
    li.append(item)
    li.append(text)
    return li
