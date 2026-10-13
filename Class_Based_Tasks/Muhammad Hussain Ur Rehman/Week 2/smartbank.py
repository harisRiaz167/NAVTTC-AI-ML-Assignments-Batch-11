from datetime import datetime

class Customer:
    def __init__(self,name,cnic,address,phone):
        self.name = name
        self.cnic = cnic
        self.address = address 
        self.phone = phone

    def show_profile(self):
        print("\n========== CUSTOMER PROFILE ==========")
        print("Name:", self.name)
        print("CNIC:", self.cnic)
        print("Phone:", self.phone)
        print("Address:", self.address)

class Account:
    def __init__(self,acc_number,pin, customer,balance=0):
        self.customer = customer
        self.account_number = acc_number
        self.pin = pin
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            print("\n ⚠️Invalid amount.")
            return
        self.balance += amount
        transaction = {
            "type": "Deposit",
            "amount": amount,
            "balance": self.balance,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
        self.transactions.append(transaction)
        print("\n✅️ Deposit successful.")
        self.transaction_slip(transaction)

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount.")
            return
        if amount > self.balance:
            print("\n⚠️ Insufficient balance.")
            return
        self.balance -= amount

        transaction = {
            "type": "Withdrawal",
            "amount": amount,
            "balance": self.balance,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        self.transactions.append(transaction)
        print("\n✅️ Withdrawal successful.")
        self.transaction_slip(transaction)

    def transaction_slip(self, transaction):
        print("\n======================================")
        print("          TRANSACTION SLIP")
        print("======================================")
        print("Account Number:", self.account_number)
        print("Customer:", self.customer.name)
        print("Transaction:", transaction["type"])
        print("Amount: Rs.", transaction["amount"])
        print("Remaining Balance: Rs.", transaction["balance"])
        print("Date:", transaction["date"])
        print("======================================")

    def mini_statement(self):
        print("\n========== MINI STATEMENT ==========")
        print("Account Number:", self.account_number)
        print("Customer:", self.customer.name)
        print("------------------------------------")

        if len(self.transactions) == 0:
            print("⚠️ No transactions found.")
            return
        else:
            for transaction in self.transactions[-5:]:
                print(transaction["date"],"|",transaction["type"],"| Rs.",transaction["amount"])
        print("------------------------------------")
        print("Current Balance: Rs.", self.balance)

    def show_balance(self):
        print("\nCurrent Balance: Rs.", self.balance)
    

class Bank:
    def __init__(self,name):
        self.name = name
        self.accounts = {}
        self.next_account_number = 1001

    def create_account(self):
        name = input("Please enter your name : ")
        cnic = int(input("Please enter your cnic : "))
        phone = int(input("Please enter your phone number : "))
        address = input("Please enter your address : ")
        pin = int(input("🔐 Enter pin : "))
        initial_deposit = int(input("Please enter initial Deposit : "))
        if initial_deposit < 0 : 
            print("\n ⚠️Initial deposit can't be negative!")
            return
        customer  = Customer(name, cnic, address,phone)
        acc_number = self.next_account_number
        self.next_account_number +=1
        account = Account(acc_number,pin, customer,initial_deposit)
        self.accounts[acc_number] = account
        print("\n✅️ Account created successfully!")
        print("#️⃣  Your Account Number is: ", acc_number)
        # bank.all_accounts()

    def find_account(self):
        accNum = int(input("PLease enter account number : "))

        if accNum in self.accounts:
            account = self.accounts[accNum]
            pin = int(input("Please enter PIN : "))
            if account.pin == pin:
                return self.accounts[accNum]   #  acc instance
            else:
                print("\n⚠️ Incorrect PIN")
                return 
        else:
            print("\n⚠️ Account Not fount!")
            return

    # def all_accounts(self):
    #      for key,acc in self.accounts.items():
    #           print(f"Account Number : {acc.account_number}")
    #           print(f"Name : {acc.customer.name}")



#############################################################################################################


        
bank = Bank("Smart Bank Pakistan")

while True:
    print("\n")
    print("======================================")
    print("       🏦 SMART BANK PAKISTAN 🏦")
    print("======================================")
    print("1. 👨 Create Account")
    print("2. 💵 Deposit Money")
    print("3. 💸 Withdraw Money")
    print("4. 📄 Mini Statement")
    print("5. 📋 Customer Profile")
    print("6. 💰 Check Balance")
    print("7. ❌ Exit")
    print("======================================")

    choice = int(input("Enter your choice: "))

    if choice == 1 :
        bank.create_account()

    elif choice == 2:
        account = bank.find_account()
        if account:
            amount = int(input("💰 Please enter deposit amount : "))
            account.deposit(amount)

    elif choice == 3:
            account = bank.find_account()
            if account:
                amount = int(input("💰 Enter withdrawal amount: "))
                account.withdraw(amount)

    elif choice == 4:
            account = bank.find_account()
            if account:
                account.mini_statement()

    elif choice == 5:
            account = bank.find_account()
            if account:
                account.customer.show_profile()

    elif choice == 6:
            account = bank.find_account()
            if account:
                account.show_balance()

    elif choice == 7:
            print("🙏 Thank you for using Smart Bank.")
            break
    
    else:
            print("❌ Invalid choice.")