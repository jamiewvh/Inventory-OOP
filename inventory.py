#========Import libraries==========
from tabulate import tabulate

#========The beginning of the class==========
class Shoe:
    """
    A class to represent a shoe in the database.

    ...

    Attributes
    __________
    country : str
        country of origin
    code : str
        unique product code
    product : str
        name of the shoe
    cost : int
        price of one unit
    quantity : int
        number of units

    Methods
    _______
    get_cost:
        Returns the cost of the shoe
    get_quantity:
        Returns the number of units in stock
    __str__:
        Returns a string representation of the shoe
        
    """

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity


    def get_cost(self):
        """Returns the cost of the shoe"""
        return self.cost

    def get_quantity(self):
        """Returns the number of units in stock"""
        return self.quantity

    def __str__(self):
        """Returns a string representation of the shoe"""
        return(
f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}")


#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []
#==========Functions outside the class==============
def read_shoes_data():
    '''
    Creates a Shoe object for each line of 'inventory.txt'.
    Appends these objects to shoe_list.

    '''

    # Read file
    try:
        with open("inventory.txt", "r") as f:
            next(f)
            for line in f:
                list = line.split(",")
                new_shoe = Shoe(list[0],list[1],list[2],
int(list[3]),int(list[4]))
                shoe_list.append(new_shoe)
        print("Data loaded successfully.")
    
    # These errors will prevent any menu functions from working.
    # They would need to be fixed outside of the application.
    except FileNotFoundError:
        print("Error: 'inventory.txt' not found. Exiting program.")
        exit()
    except ValueError:
        print("Error when loading numerical data. Exiting program.")
        exit()


def capture_shoes():
    '''
    Creates a Shoe object based on user input.
    Appends this object to shoe_list, then updates 'inventory.txt'.

    '''

    # Take input
    ns_country = input("Enter country of origin:")
    code_good = False
    while code_good == False:
        ns_code = input("Enter 8-digit product code:")
        if len(ns_code) == 8:
            code_good = True
        else:
            print("The code must be 8 digits. Enter again:")
    ns_prod = input("Enter product name:")
    cost_good = False
    while cost_good == False:
        try:
            ns_cost = int(input("Enter cost per unit:"))
            cost_good = True
        except ValueError:
            print("The cost must be a number. Try again.")
    q_good = False
    while q_good == False:
        try:
            ns_quantity = int(input("Enter number of units:"))
            q_good = True
        except ValueError:
            print("The quantity must be a number. Try again.")
    
    # Update list
    n_shoe = Shoe(ns_country, ns_code, ns_prod, ns_cost, ns_quantity)
    shoe_list.append(n_shoe)

    # Update file
    with open("inventory.txt", "w") as f:
        f.write("Country,Code,Product,Cost,Quantity\n")
        for shoe in shoe_list:
            f.write(shoe.__str__() + "\n")

    # Confirmation message
    print("New shoe added to database.")


def view_all():
    '''
    Prints shoe_list in user-friendly form.

    '''

    table = []
    for shoe in shoe_list:
        lst = [shoe.country,shoe.code,shoe.product,shoe.cost,shoe.quantity]
        table.append(lst)
    print(tabulate(table, ["Country","Code","Product","Cost","Quantity"]))


def re_stock():
    '''
    Finds the object in shoe_list with the lowest quantity value.
    Takes user input on whether to update this value.

    '''
    # Find shoe to be restocked
    q_list = []
    for shoe in shoe_list:
        q_list.append(shoe.get_quantity())
    for shoe in shoe_list:
        if shoe.get_quantity() == min(q_list):
            restock = shoe
    print("Lowest stock shoe:")
    print(restock.__str__())

    # Ask for input
    ch_good = False
    while ch_good == False:
        choice = input("Restock shoe? Y/N").lower()
        if choice == "y":
            ch_good= True
            num_good = False
            while num_good == False:
                try:
                    num = int(input("How many units to restock?"))
                    num_good = True
                    restock.quantity += num
                    # Update file
                    with open("inventory.txt", "w") as f:
                        f.write("Country,Code,Product,Cost,Quantity\n")
                        for shoe in shoe_list:
                            f.write(shoe.__str__() + "\n")
                    # Confirmation message
                    print("Shoe restocked:")
                    print(restock.__str__())
                except ValueError:
                    print("You must enter a number.")
        elif choice == "n":
            ch_good = True
            print("Returning to menu.")
        else:
            print("Please input Y/N.")     


def search_shoe():
    '''
    Prints information for an object in shoe_list with the same code as input.
    
    '''
    code_good = False
    while code_good == False:
        search_code = input("Enter 8 digit shoe code:")
        if len(search_code) != 8:
            print("The code must be 8 digits.")
        else:
            for shoe in shoe_list:
                if shoe.code == search_code:
                    print("Printing search results:")
                    print(shoe.__str__())
                    code_good = True
            if code_good == False:
                print("Shoe not found. Please enter a valid code.")

        
def value_per_item():
    '''
    Prints a table with total value of each object in shoe_list.
    
    '''
    table = []
    for shoe in shoe_list:
        lst = [shoe.product,shoe.code,shoe.cost*shoe.quantity]
        table.append(lst)
    print(tabulate(table, ["Product","Code","Total Value"]))


def highest_qty():
    '''
    Finds the object in shoe_list with the highest quantity value.
    Prints a message about it being on sale.
    
    '''
    q_list = []
    for shoe in shoe_list:
        q_list.append(shoe.get_quantity())
    for shoe in shoe_list:
        if shoe.get_quantity() == max(q_list):
            sale = shoe
    print(f"{sale.product} is on sale!")
    
#==========Main Menu=============
# This function runs on startup since it is required for all other functions.
read_shoes_data()
# Menu
while True:
    menu = input('''
Welcome to the inventory application (currently shoes-only). Choose one:
a - Add a shoe
d - View the shoe data
r - Re-stock shoes
s - Search for a shoe
v - Show value of stock
q - Put shoes on sale
e - Exit the application
''').lower()

    if menu == "a":
        capture_shoes()
    elif menu == "d":
        view_all()
    elif menu == "r":
        re_stock()
    elif menu == "s":
        search_shoe()
    elif menu == "v":
        value_per_item()
    elif menu == "q":
        highest_qty()
    elif menu == "e":
        print("Goodbye.")
        exit()
    else:
        print("Error - wrong input.")