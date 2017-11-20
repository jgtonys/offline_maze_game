import UserController,os,maze
import Viewer,TestingReport

def main():
    while True:
        Viewer.main_view("MAZE")
        ch = Viewer.main_select()
        if ch == '1': UserController.login()
        elif ch == '2': UserController.register()
        elif ch == '3': exit(1)
        elif ch == '4': TestingReport.report()
        else: print("INVALID INPUT!")

main()
