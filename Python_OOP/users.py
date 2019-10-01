Assignment: User
Objectives:
Practice creating a class and making instances from it
Practice accessing the methods and attributes of different instances
______________________________________________________________________

class User:
    def __init__(self, user, account): 
        self.name = user 
        self.account = BankAccount(0.02, 500)


    def make_deposit(self, amount): 

        self.account.deposit(amount)
        return self 

    
    def make_withdrawal(self, amount):

        self.account.withdraw(amount)
        return self


    def display_user_balance(self):  
        self.account.display_account_info()
        return self 

     def transfer_money(self, other_user, amount):
        self.account.yield_interest(account_balance)
        return self 


class BankAccount: 
    def __init__(self,  int_rate, balance):
        
        self.account_balance = 0 
        self.int_rate = 0.02

        
    def deposit(self,amount):
        self.account_balance += amount 
        return self 


    def withdraw(self, amount): 
        self.account_balance -= amount 
        return self  
    

    def display_account_info(self):
        print(self.account_balance) 
        return self 
        

    def yield_interest(self, account_balance):
        self.account_balance = self.account_balance + (self.account_balance * self.int_rate)
        return self



Mary = User("Mary", "naanepmaryg@gmail.com")
# Devonte = User("Devonte")
# Howard = User("Howard")

Mary.make_deposit(1500).make_deposit(100).make_deposit(300).make_withdrawal(500).display_user_balance()

Mary.transfer_money(Devonte, 30)
Mary.display_user_balance()

# Mary.make_withdrawal(300)
# Devonte.make_withdrawal(200)

# Mary.display_user_balance()
# Devonte.display_user_balance()
