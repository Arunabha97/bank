__author__ = 'user'

import database
import validate
from classes import Account,Savings,Current,Fixed_Deposit,Address
import database_admin as db_admin

def change_address(id):
    ch = 1
    addr = ""

    print("-- Menu --")
    print("1. Change Address Line 1")
    print("2. Change Address Line 2")
    print("3. Change State")
    print("4. Change City")
    print("5. Change Pincode")
    print("6. Quit")

    while ch != 6:

        try:
            ch = int(input())
        except:
            print("ERROR: Invalid Choice")
            ch = 1
            continue

        if ch == 1:
            addr = input("Enter New Address Line 1: ")

        elif ch == 2:
            addr = input("Enter New Address Line 2: ")

        elif ch == 3:
            addr = input("Enter New State: ")

        elif ch == 4:
            addr = input("Enter New City: ")

        elif ch == 5:
            addr = input("Enter New Pincode: ")

        elif ch == 6:
            break

        database.change_address_customer(ch,id,addr)

def get_new_account(ch,id):
    account = None
    acc_type = None
    msg = "Enter Balance "
    term = None
    if ch == 1:
        account = Savings()
        acc_type = "savings"
        msg += ": Rs "
    elif ch == 2:
        account = Current()
        acc_type = "current"
        msg += "(min 5000): Rs "
    elif ch == 3:
        account = Fixed_Deposit()
        acc_type = "fd"
        msg += "(min 1000): Rs "
    else:
        return None

    balance = int(input(msg))
    while account.open_account(balance) == False:
        balance = int(input("\nEnter Valid Balance: Rs"))

    if ch == 3:
        try:
            term = int(input("\nEnter Deposit Term (Min 12 months): "))
        except:
            print("ERROR: Invalid Deposit term")
            return
        while term < 12:
            term = int(input("ERROR: Please Enter a valid Deposit Term!!"))

    account.set_account_type(acc_type)
    if isinstance(account,Fixed_Deposit):
        account.set_deposit_term(term)
    return account

def open_new_account(id):
    account = None
    print("\n --- Menu --- ")
    print("1. Open Savings Account")
    print("2. Open Current Account")
    print("3. Open Fixed Deposit Account")

    try:
        ch = int(input("Enter Choice: "))
    except:
        print("ERROR: Invalid Choice")
        return

    account = get_new_account(ch,id)
    if account is not None:
        database.open_new_account_customer(account,id)
        if ch == 3:
            res = db_admin.get_fd_report(id)
            print("Account No \t\t\t\t Amount \t\t\t\t Deposit Term")
            for i in range(0,len(res)):
                print(res[i][0],"   \t\t\t\t\t Rs",res[i][1],"   \t\t\t\t   ",res[i][2])

    else:
        print("ERROR: Invalid Choice")


def deposit_money(id):
    try:
        acc_no = int(input("Enter your account No: "))
    except:
        print("ERROR: Invalid Account No")
        return
    account = database.get_all_info_account(acc_no,id,"deposit")
    if account is not None:
        try:
            amount = int(input("Enter amount to Deposit: Rs "))
        except:
            print("ERROR: Invalid Amount")
            return
        if account.deposit(amount) == True:
            database.money_deposit_customer(account,amount)
            print("Rs ",amount,"Successfully deposited");
            print("Balance : Rs ",account.get_balance())

    else:
        print("ERROR: Account No doesn't match")

def withdraw_money(id):
    try:
        acc_no = int(input("Enter your account No: "))
    except:
        print("ERROR: Invalid Account No")
        return
    account = database.get_all_info_account(acc_no,id,"withdraw")
    if account is not None:
        if account.get_withdrawals_left() == 0 and account.get_account_type() == "savings":
            print("ERROR: You have exceeded withdrawals(10) for this month")

        else:
            try:
                amount = int(input("Enter amount to Withdraw: "))
            except:
                print("ERROR: Invalid Amount")
                return
            if account.withdraw(amount) == True:
                database.money_withdraw_customer(account,amount,"withdraw")
                print("Rs ",amount,"Successfully withdrawn");
                print("Balance : Rs ",account.get_balance())

    else:
            print("ERROR: Account No doesn't match")

def print_statement(id):
    try:
        acc_no = int(input("Enter your account No: "))
    except:
        print("ERROR: Invalid Account No")
        return
    account = database.get_all_info_account(acc_no,id,"statement")
    if account is not None:
        print("Enter Dates  <dd-mmm-yyyy>")
        date_from = input("Date From: ")
        date_to = input("\nDate To: ")
        if validate.validate_date(date_from,date_to) == True:
            res = database.get_transactions_account(acc_no,date_from,date_to)
            print("Date \t\t\t Transaction Type \t\t\t Amount \t\t\t Balance \t")
            for i in range(0,len(res)):
                print(res[i][0].strftime("%d-%b-%Y")," \t\t\t ",res[i][1]," \t\t\t ",res[i][2]," \t\t\t ",res[i][3])
        else:
            print("ERROR: Please Enter Valid Dates!")

def close_account(id):
    try:
        acc_no = int(input("\nEnter Account No to close: "))
    except:
        print("ERROR: Invalid Account No")
        return
    account = database.get_all_info_account(acc_no,id,"close")
    if account is not None:
        database.close_account_customer(account)
    else:
        print("\nSorry Account No. doesn't match")
