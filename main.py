import functions
from os import system
import database
import cx_Oracle
from connection import con,cur

def main():

    database.make_all_tables()
    database.reset_withdrawals()
    choice = 1

    print("\n##### Welcome To ONLINE BANKING TERMINAL #####\n")
    while choice != 0:
        print("\t--- Main Menu ---\n ")
        print("1. Sign Up (New Customer) ")
        print("2. Sign In (Existing Customer) ")
        print("3. Admin Sign In ")
        print("4. Quit ")
        print("\nEnter Your Choice: ", end='')
        try:
            choice = int(input())
            system('CLS')
            print("\n##### Welcome To ONLINE BANKING TERMINAL #####\n")
        except:
            system('CLS')
            print("\n##### Welcome To ONLINE BANKING TERMINAL #####\n")
            print("\tERROR: Invalid Input! ENTER AGAIN\n")
            choice = 1
            continue

        if choice == 1:
            functions.sign_up();

        elif choice == 2:
            functions.sign_in();

        elif choice == 3:
            functions.admin_sign_in();

        elif choice == 4:
            print("Saving Transaction ...\nClosing Terminal ...\n\n")
            break

        else:
            system('CLS')
            print("\n##### Welcome To ONLINE BANKING TERMINAL #####")
            print("ERROR: Unknown Choice! ENTER AGAIN\n")


main()
