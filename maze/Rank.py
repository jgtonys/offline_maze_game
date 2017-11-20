import os
import DBcon
import Viewer

def get_ranking():
    rows = DBcon.get_all_db()
    Viewer.main_view("MAZE RANKING")
    print("등수 \t"+"{:<24}".format("ID"),end="\t")
    print("{:<6}".format("LV"),end="\t")
    print("{:<6}".format("Coin"),end="\t")
    print("{:<6}".format("Elapsed Time"),end="\n\n")
    for i in range(len(rows)):
        print(str(i+1)+"등\t",end="")
        for j in range(len(rows[i])):
            if j==0:
                if rows[i][j] == 99999.0:
                    print("없음",end = "")
                else:
                    print("{:<24}".format(rows[i][j]),end="\t")
            else:
                if rows[i][j] == 99999.0:
                    print("없음",end = "")
                else:
                    print("{:<6}".format(rows[i][j]),end="\t")
        print()
    input("\n\n돌아가려면 아무키나 누르세요")
    os.system("cls")
