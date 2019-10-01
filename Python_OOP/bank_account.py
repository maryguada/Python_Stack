Assignment: BankAccount
Objectives
Practice writing classes
_______________________________

class BankAccount: 

    def __init__(self, username, int_rate, balance):
        self.name = username
        self.account_balance = balance
        self.int_rate = 0.05 
        # self.account_balance = (self.account_balance)+(self.account_balance*self.int_rate)

        
    def deposit(self,amount):
        self.account_balance += amount 
        return self 


    def withdraw(self, amount): 
        self.account_balance -= amount 
        return self  
    
    def display_account_info(self):
        print(self.name, self.account_balance) 
        return self 
        

    def yield_interest(self, account_balance):
        self.account_balance = self.account_balance + (self.account_balance * self.int_rate)
        return self
        
