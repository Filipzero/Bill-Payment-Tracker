import re
from datetime import datetime
import mysql.connector
from decimal import Decimal, InvalidOperation


mydb = mysql.connector.connect(
        host= 'localhost',
        user='your username', # your username!
        password='you password', # your password!
        database='Bills' # ******* THE NAME OF THE DATABASE THAT IS BEING USED TO STORE THE INFORMATION !!! *******
)


mycursor = mydb.cursor(buffered=True)


class User:

    # Initialize attributes of the class User with the constructor __init__ so that we can add as many users as we want. 
    # Attributes stay the same amongst different objects, but their values may change.

    def __init__(self, name, email): # The keyword self is used as a link between objects and methods and it allows us to store the values of an object. Otherwise I would have gotten an error saying I gave 3 positional arguments while it has 2. That is happening, because the method __init__ receives one more argument than what I explicitly passed and that is the object itself (In this occasion the object user1).

        self.name = name
        self.email = email

        # Every time we create a new object User, the bills list is created anew and begins with a blank list of bills. This one does not affect the data base. It exists only in memory.
        self.bills = []

    # In this Method, when we call the object with its distinct values, the bills are going to be stored in the self.bills list
    def add_bills(self, bills):
        
        self.bills.append(bills)


    # I'm passing mydb and mycursor as arguments because they do not belong inside the class.
    def store_to_db(self, mydb, mycursor): 
        # Checking if a name already exists
        mycursor.execute("SELECT user_id FROM Users WHERE name = %s", (self.name,))
        result = mycursor.fetchone()
    
        if result:
            print(f"User {self.name} already exists in the database.")
            return result[0]  # Return existing user ID

        else:
            sql = "INSERT INTO Users (name, email) Values(%s, %s)"
            val = (self.name, self.email)
            mycursor.execute(sql, val)
            mydb.commit() # If I hadn't typed this then it would be stored in short memory.
            user_id = mycursor.lastrowid  # Get auto-incremented user ID. I need it for linking between user and bill
            return user_id
    

class Bill:


    def __init__(self, provider, amount, due_date):
        
        self.provider = provider
        self.amount = amount
        self.due_date = due_date
        #self.category = category


    def db_bills(self, mydb, mycursor, user_id):

        sql2 = "INSERT INTO Invoices (provider, amount, due_date, user_id) Values (%s, %s, %s, %s)"
        val2 = (self.provider, self.amount, self.due_date, user_id)
        mycursor.execute(sql2, val2)
        mydb.commit()
        bill_id = mycursor.lastrowid
        return bill_id


    # This function and the others below similar to this are if I need to just print an object of the class Bill (e.g., bill) and say print(bill) -> internally it does print(str(bill)) and i dont have to type print(bill.provider)
    def __str__(self):
       
        return f"Provider: {self.provider}, Amount: {self.amount} €, Due_date: {self.due_date}" # {self.category}"


class WaterBill(Bill):


    def __init__(self, provider, amount, due_date, consumption_m3):

        super().__init__(provider, amount, due_date)
        self.consumption_m3 = consumption_m3
    

    def db_waterbill(self, mydb, mycursor, user_id):

        sql3 = "INSERT INTO WaterBills (provider, amount, due_date, consumption_m3, user_id) Values (%s, %s, %s, %s, %s)"
        val3 = (self.provider, self.amount, self.due_date, self.consumption_m3, user_id)
        mycursor.execute(sql3, val3)
        mydb.commit()



    def __str__(self):
        
        return f"Water bill from {self.provider}: {self.amount}€ due {self.due_date}, usage={self.consumption_m3} m³"


class ElectricityBill(Bill):


    def __init__(self, provider, amount, due_date, kwh_used):

        super().__init__(provider, amount, due_date)
        self.kwh_used = kwh_used


    def db_electricitybill(self, mydb, mycursor, user_id):

        sql4 = "INSERT INTO ElectricityBills (provider, amount, due_date, kwh_used, user_id) Values (%s, %s, %s, %s, %s)"
        val4 = (self.provider, self.amount, self.due_date, self.kwh_used, user_id)
        mycursor.execute(sql4, val4)
        mydb.commit()


    def __str__(self):
        return f"Electricity bill from {self.provider}: {self.amount}€ due {self.due_date}, usage={self.kwh_used} kWh"


class InternetBill(Bill):

    def __init__(self, provider, amount, due_date, data_gb):

        super().__init__(provider, amount, due_date)
        self.data_gb = data_gb


    def db_internetbill(self, mydb, mycursor, user_id):

        sql5 = "INSERT INTO InternetBills (provider, amount, due_date, data_gb, user_id) Values (%s, %s, %s, %s, %s)"
        val5 = (self.provider, self.amount, self.due_date, self.data_gb, user_id)
        mycursor.execute(sql5, val5)
        mydb.commit()


    def __str__(self):
        return f"Internet bill from {self.provider}: {self.amount}€ due {self.due_date}, usage={self.data_gb} GB"


class Payment:


    def __init__(self, amount, date, method):

        self.amount = amount # the amount to pay
        self.date = date # the date of payment
        self.method = method  # e.g. "card", "cash"


    def db_payment(self, mydb, mycursor, bill_id):

        sql6 = "INSERT INTO Payments (amount, payment_date, method, bill_id) VALUES (%s, %s, %s, %s)"
        val6 = (self.amount, self.date, self.method, bill_id)
        mycursor.execute(sql6, val6)
        mydb.commit()


class BillManager:
    

    def __init__(self, month, year):

        self.month = month
        self.year = year


    def get_monthly_expenses(self, mycursor, user_id):

         sql7 = "SELECT SUM(p.amount) as total FROM Payments p JOIN Invoices i ON p.bill_id = i.id WHERE MONTH(p.payment_date) = %s AND YEAR(p.payment_date) = %s AND i.user_id = %s"
         val7 = (self.month, self.year, user_id)
         mycursor.execute(sql7, val7)
         fetch_query = mycursor.fetchone()

         # I have to create an if statement, because I want it to return the sum (which is in a tuple), but if it doesn't have a sum it will return None. 
         return fetch_query[0] if fetch_query[0] else 0


    def is_paid(self, mycursor, user_id, month=None, year=None):
        
        # Default to self.month and self.year if no month/year are passed as arguments       
        month = month or self.month
        year = year or self.year
        
        sql8 = "SELECT p.id, p.bill_id, i.due_date FROM Payments p JOIN Invoices i ON p.bill_id = i.id WHERE MONTH(i.due_date) = %s AND YEAR(i.due_date) = %s AND i.user_id = %s"
        val8 = (month, year, user_id)
        mycursor.execute(sql8, val8)
        fetch_query2 = mycursor.fetchall()
        
        for payment_id, bill_id, due_date in fetch_query2: 
            if due_date.month == month:
                print(f"\n--------Bill with this id: '{payment_id}' is paid--------")
            else:
                print("\nNot paid")

        if not fetch_query2:
            print("No bills found for this user and month.")
        return

def Val_email(email):
    
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)


def Validator(input):
    
    return input.replace(" ", "").isalpha()



# User
print("User")

while True:
    name = input("Enter your name: ").capitalize()
    if Validator(name) == False:
        print(f"\n{name} is not valid.\nNames should only contain letters.\n")
    else:
        break


while True:
    email = input("Enter your email: ")
    if Val_email(email) == None:
        print(f"\n{email} is not valid.\nTry again (e.g. smth@gmail.com)\n")
    else:
        break


user1 = User(name, email) # Create an object. In this case user1 with name and email given from the input above.

user_id = user1.store_to_db(mydb, mycursor)



print("\n")
# Bill
print("Bill information")

format_data = "%d/%m/%Y"

while True:
    
    W_E_I = input("What kind of bill is it ? (Water, Electricity or Internet): ").capitalize()
    
    if W_E_I not in ["Water", "Electricity", "Internet"]:
        print("Invalid type. Please enter Water, Electricity or Internet")
        continue


    if W_E_I == "Water":

        while True:

            provider = input("Enter your provider: ").capitalize()

            if Validator(provider) == False:
                print(f"\n{provider} is not valid.\nProvider should only contain letters.")
        
            else:
                 break
                
        while True:
        
            try:
                amount = Decimal(input("Enter amount: "))
                break
   
            except InvalidOperation:
                print("\n")
                print("Please enter the amount again")
                print("\n")
    
        while True:

            try:
                date = input("Enter due_date(e.g. 10/05/2004 (DD/MM/YYYY)): ")
                due_date = datetime.strptime(date, format_data).date()
                break
        
            except ValueError:
                print("\n")
                print("Please enter a valid date DD-MM-YYYY")
                print("\n")

        while True:

            try:
                consumption_m3 = Decimal(input("Enter the cubic meters of water consumption: "))
                break
            
            except InvalidOperation:
                print("\n")
                print("Please enter cubic meters")
                print("\n")

        bill = WaterBill(provider, amount, due_date, consumption_m3)
        database_waterbill = bill.db_waterbill(mydb, mycursor, user_id)


    elif W_E_I == "Electricity":
        
        while True:

            provider = input("Enter your provider: ").capitalize()
        
            if Validator(provider) == False:
                print(f"{provider} is not valid.\nProvider should only contain letters.")
        
            else:
                break

        while True:
        
            try:
                amount = Decimal(input("Enter amount: "))
                break
   
            except InvalidOperation:
                print("\n")
                print("Please enter the amount again")
                print("\n")
    
        while True:

            try:
                date = input("Enter due_date(e.g. 10/05/2004 (DD/MM/YYYY)): ")
                due_date = datetime.strptime(date, format_data).date()
                break
        
            except ValueError:
                print("\n")
                print("Please enter a valid date DD-MM-YYYY")
                print("\n")

        while True:
            
            try:
                kwh_used = Decimal(input("Enter kWh used: "))
                break
            
            except InvalidOperation:
                print("\n")
                print("Please enter the kWh used again.")
                print("\n")

        bill = ElectricityBill(provider, amount, due_date, kwh_used)
        database_electricitybill = bill.db_electricitybill(mydb, mycursor, user_id)

    elif W_E_I == "Internet":

        while True:

            provider = input("Enter your provider: ").capitalize()
        
            if Validator(provider) == False:
                print(f"{provider} is not valid.\nProvider should only contain letters.")
        
            else:
                break

        while True:
        
            try:
                amount = Decimal(input("Enter amount: "))
                break
   
            except InvalidOperation:
                print("\n")
                print("Please enter the amount again")
                print("\n")
    
        while True:

            try:
                date = input("Enter due_date(e.g. 10/05/2004 (DD/MM/YYYY)): ")
                due_date = datetime.strptime(date, format_data).date()
                break
        
            except ValueError:
                print("\n")
                print("Please enter a valid date DD-MM-YYYY")
                print("\n")

        while True: 

            try:
                data_gb = Decimal(input("Enter GB used: "))
                break

            except InvalidOperation:
                print("\n")
                print("Please enter your GB consumption again.")
                print("\n")

        bill = InternetBill(provider, amount, due_date, data_gb)
        database_internetbill = bill.db_internetbill(mydb, mycursor, user_id)
    
    break

#bill1 = Bill(provider, amount, due_date) # Object bill1. ***I don't need this because the object will only inherit the attributes of the class Bill and is outside of my while loop.
store_bill = user1.add_bills(bill) # I could have let it be user1.add_bills(bill), but I named it. I called the add_bill() method and store the bill object. ***Also, I could delete this since it only exists in memory and doesn't list all my bills.

bill_id = bill.db_bills(mydb, mycursor, user_id) # I store my bills, but also acts as a bill_id inside class Payments so that I can link them.


print("\n")
# Payment
print("Payment")

while True:
    
        while True:
            try:
                amount_payed = Decimal(input("Enter amount being payed: "))
                break

            except InvalidOperation:
                print("\n")
                print("Please enter the amount again")
                print("\n")

        while True:

            try:
                date = input("Enter the date that the bill is payed(e.g. 10/05/2004 (DD/MM/YYYY)): ")
                date_payed = datetime.strptime(date, format_data).date()
                break

            except ValueError:
                print("\n")
                print("Please enter a valid date DD-MM-YYYY")
                print("\n")
   
        while True:
            payments_options = ['Cash', 'Credit Card', 'Debit Card']
            method = input("Paying method: Cash, Credit Card, Debit Card: ").title()
            
            if method not in payments_options:
                print("\nPlease choose a way of payment again\n")
                continue
            
            else:
                break
        break

payment1 = Payment(amount_payed, date_payed, method) # Creation of an object again

database_payment = payment1.db_payment(mydb, mycursor, bill_id)


print("\n")
#BillManager
print("Bill Manager")


while True:

    while True:
        
        try:
            month = input("Choose a month to calculate expenses (e.g., '05'): ")
            month_obj = datetime.strptime(month, "%m")
            month_inp = month_obj.month
            break

        except ValueError:
            print("\n")
            print("Please enter a month like so: '05'")
            print("\n")


    while True:

        try:
            year = input("Choose the year of the month (e.g., '2025'): ")
            year_obj = datetime.strptime(year, "%Y")
            year_inp = year_obj.year
            break

        except ValueError:
            print("\n")
            print("Please enter a year like so: '2025'")
            print("\n")

    
    break

manager = BillManager(month_inp, year_inp)
calc_exp = manager.get_monthly_expenses(mycursor, user_id)

# Check if a bill is paid

while True:
    
    li=["y", "n"]
    check = input("Do you want to check if some bill is paid (y/n):  ").lower()

    
    if check == li[0]:

        while True:
        
            try:
                month = input("Check if the bill of some month is paid (e.g., '05'): ")
                month_obj = datetime.strptime(month, "%m")
                check_month = month_obj.month
                break

            except ValueError:
                print("\n")
                print("Please enter a month like so: '05'")
                print("\n")


        while True:

            try:
                year = input("Choose the year of the month (e.g., '2025'): ")
                year_obj = datetime.strptime(year, "%Y")
                check_year = year_obj.year
                break

            except ValueError:
                print("\n")
                print("Please enter a year like so: '2025'")
                print("\n")
        # I have to put the variable check_bills_paid here, because if someone types anything other than y, the variables check_month and check_year won't exist.
        check_bills_paid = manager.is_paid(mycursor, user_id, check_month, check_year)
        break

    elif check == li[1]:
        print("Ok 👍")
        break

    else:
        print("Please type 'y' for yes or 'n' for no")
        continue


print("\nInformation Provided\n")
print(f"User_1_name: {user1.name}\nUser_1_email: {user1.email}") # User_1_bills : {user1.bills[0]})
for i in user1.bills: # prints every bill stored in user1
    print(f"User_1_bills: {i}")
print("\n")
print(f"Bill_provider: {bill.provider}\nBill_amount: {bill.amount}€\nBill_due_date: {bill.due_date}")  # Bill_category : {bill.category} Bill
if isinstance(bill, WaterBill):
    print(f"Consumption of water: {bill.consumption_m3} m³")
elif isinstance(bill, ElectricityBill):
    print(f"kWh used: {bill.kwh_used} kWh")
elif isinstance(bill, InternetBill):
    print(f"Data used: {bill.data_gb} GB")
print("\n")
print(f"Payment_1_amount: {payment1.amount}€\nPayment_1_date: {payment1.date}\nPayment_1_method: {payment1.method}")
print("\n")
if calc_exp == 0:
    print("No payments recorded for this month!")
else:
    print(f"Expenses on {manager.month}/{manager.year}: {calc_exp:.2f}€")

while True:

    list_tables = ["n", "invoice", "water", "electricity", "internet", "payment"]
    print("\n")
    print_details = input("If you want to see more details on a specific table type (invoice, water, electricity, internet or payment) and if not type 'n': ").lower()
    print("\n")
    
    while True:
        if Validator(print_details) == False:
            print(f"\nPlease choose between 'n', 'invoice', 'water', 'electricity', 'internet', 'payment'\n")
            continue
        else:
            break

    if print_details == list_tables[0]:
        break

    elif print_details == list_tables[1]:
        mycursor.execute("SELECT * FROM Invoices WHERE user_id = %s", (user_id,)) # ***** I have to use (user_id,) to make it a tuple, because it gives an error : mysql.connector.errors.ProgrammingError: Could not process parameters: int(1), it must be of type list, tuple or dict ****
        tables = mycursor.fetchall()
        print("------Invoices------\n")
        for (id_, provider, amount, due_date, user_id_) in tables:
            print(f"ID: {id_} | Provider: {provider} | Amount: {amount} € | Due date: {due_date}")

    elif print_details == list_tables[2]:
        mycursor.execute("SELECT * FROM WaterBills WHERE user_id = %s", (user_id,))
        tables = mycursor.fetchall()
        print("------Water Bills------\n")
        for (id_, provider, amount, due_date, consumption_m3, user_id_) in tables:
            print(f"ID: {id_} | Provider: {provider} | Amount: {amount} € | Due date: {due_date} | Consumption: {consumption_m3} m³")

    elif print_details == list_tables[3]:
        mycursor.execute("SELECT * FROM ElectricityBills WHERE user_id = %s", (user_id,))
        tables = mycursor.fetchall()
        print("------Electricity Bills------\n")
        for (id_, provider, amount, due_date, kwh_used, user_id_) in tables:
            print(f"ID: {id_} | Provider: {provider} | Amount: {amount} € | Due date: {due_date} | Usage: {kwh_used} kWh")
    
    elif print_details == list_tables[4]:
        mycursor.execute("SELECT * FROM InternetBills WHERE user_id = %s", (user_id,))
        tables = mycursor.fetchall()
        print("------Internet Bills------\n")
        for (id_, provider, amount, due_date, data_gb, user_id_) in tables:
            print(f"ID: {id_} | Provider: {provider} | Amount: {amount}€ | Due: {due_date} | Data: {data_gb} GB")

    elif print_details == list_tables[5]:
        mycursor.execute("SELECT p.* FROM Payments p JOIN Invoices i ON p.bill_id = i.id WHERE i.user_id = %s", (user_id,))
        tables = mycursor.fetchall()
        print("------Payments------\n")
        for (id_, amount, payment_date, method, bill_id) in tables:
            print(f"ID: {id_} | Amount: {amount} | Payment_date: {payment_date} | Method of payment: {method} | Bill ID: {bill_id}")


