class Bank:
    def __init__(self):
        self.balance = 0.0
        print ("The account is created")
        
    def deposit(self):
        amount = float(input("Enter the amount to be deposit: "))
        self.balance = self.balance + amount
        print ("Deposit is successful and the balance in the account is %f" % self.balance)
    
    def withdraw(self):
        amount = float(input("Enter the amount to withdraw: "))
        if (self.balance >= amount):
            self.balance = self.balance - amount
            print ("The withdraw is successfull and balance is %f" % self.balance)
        elif(amount>self.balance):
            # self.balance=self.balance-amount
            print("withdraw money exceeded available balance")
        else:
            print ('Insuficient Balance')
    
    def enquiry(self):
        print ("Balance in the acount is %f" % self.balance)
acc = Bank()       
while(True):
   
    print("please enter your choice")
    s=input()
    if(s=="exit"):
        break
    if(s=="deposit"):
        acc.deposit()
    elif(s=="withdraw"):
        acc.withdraw()
    elif(s=="enquiry"):
        acc.enquiry()
    else:
        print("You selected wrong choice")



    # acc = Bank()
    # acc.deposit()
    # acc.withdraw()
    # # y = map(deposit,[100,50,30,50])
    # # print(y)
    # # z = map(withdraw,[1,2,5,2,60])
    # # print(z)
    # acc.enquiry()