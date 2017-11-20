import sqlite3 as sql

def valid_id_check(username,password):
    with sql.connect('USERINFO.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM USERINFO WHERE ID = ?',(username,))
        RPW = cur.fetchall()
        data = len(RPW)
    con.commit()
    con.close()
    if data == 0: return 2
    elif password == RPW[0][1]: return RPW
    else: return 3

def db_refresh(username):
    with sql.connect('USERINFO.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM USERINFO WHERE ID = ?',(username,))
        RPW = cur.fetchall()
    con.commit()
    con.close()
    return RPW

def db_register(username,password):
    with sql.connect('USERINFO.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO USERINFO(ID,PW,LV,COIN,CH,ET) VALUES(?,?,?,?,?,?)",(username,password,1,0,0,99999,))
        cur.execute("INSERT INTO USERCH(id,username,contents) VALUES(?,?,?)",(0,username,"기본스킨",))
    con.commit()
    con.close()

def showinventory(user):
    con = sql.connect('USERINFO.db')
    cur = con.cursor()
    cur.execute("SELECT id,contents FROM USERCH WHERE username = ?",(user.username,))
    return cur.fetchall()

def skinchange(user,ch):
    with sql.connect("USERINFO.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE USERINFO SET CH = ? WHERE ID = ?",(ch,user.username))
    con.commit()
    con.close()

def db_update(username,_lv,_coin,_et):
    Tmp = int(_lv/3)
    rtmp = ((Tmp*6)+10)*(1.5)
    with sql.connect('USERINFO.db') as con:
        cur = con.cursor()
        if rtmp > _et:
            cur.execute("UPDATE USERINFO SET LV=?,COIN=?,ET=? WHERE ID = ?", (_lv+1,_coin,99999,username,))
        else:
            cur.execute("SELECT ET FROM USERINFO WHERE ID = ?",(username,))
            data = cur.fetchall()
        if data[0][0] == 99999:
            cur.execute("UPDATE USERINFO SET LV=?,ET = ?,COIN = ? WHERE ID = ?", (_lv,_et,_coin,username,))
        elif data[0][0] > float(_et):
            cur.execute("UPDATE USERINFO SET LV=?,ET = ?,COIN = ? WHERE ID = ?", (_lv,_et,_coin,username,))
        else:
            cur.execute("UPDATE USERINFO SET COIN = ? WHERE ID = ?", (_coin,username,))
    con.commit()
    con.close()

def db_shopping(user,text):
    with sql.connect('USERINFO.db') as con:
        cur = con.cursor()
        cur.execute("UPDATE USERINFO SET CH=?,COIN=? WHERE ID = ?", (user.character,user.coin,user.username,))
        cur.execute("INSERT INTO USERCH(id,username,contetns) VALUES(?,?,?)", (user.character,user.username,text,))
    con.commit()
    con.close()

def get_all_db():
    con = sql.connect('USERINFO.db')
    cur = con.cursor()
    cur.execute("SELECT ID,LV,COIN,ET FROM USERINFO ORDER BY LV DESC,ET ASC")
    return cur.fetchall()

def show_id_list():
    con = sql.connect('USERINFO.db')
    cur = con.cursor()
    cur.execute("SELECT ID,LV FROM USERINFO")
    return cur.fetchall()
