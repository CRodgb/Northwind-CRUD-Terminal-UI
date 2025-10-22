import mysql.connector
import datetime
import time

db = mysql.connector.connect(
    host='localhost',
    user='nwcrud',
    password='admin',
    database='northwind'
)

mycursor = db.cursor()

def check_product_discontinued(product_id:str):

    check = True

    while check == True:

        product_id = check_number_pos(product_id)
        
        query = "SELECT Discontinued FROM Products WHERE ID = %s"
        mycursor.execute(query, (product_id,))

        result = mycursor.fetchone()
        if result is None:
            print("Please enter a valid product ID.")
            product_id = input()
        else:
            result = result[0]

        # If product is discontinued, cancel ordering process
        if result == 1:
            print("We're sorry, this product has been discontinued.")
            time.sleep(2)
            return
        elif result == 0:
            check = False
            return product_id
        


#TEST
def check_number_pos(user_input:str):

    # Check int
    check = True
    while check == True:
        try:
            int(user_input)
            user_input = int(user_input)

            if user_input > 0:

                check = False
                return str(user_input)

            else:

                print("Please enter a positive number.")
                user_input = input()
                
        except:

                print("Please enter a NUMBER.")
                user_input = input()


def check_id_exists(id_to_check: str, table_name: str, id_column: str, friendly_name: str):
    """
    Checks if a given ID exists in a specific table.
    Loops until a valid ID is provided.
    """
    check = True
    while check:
        id_to_check = check_number_pos(id_to_check)
        
        query = f"SELECT {id_column} FROM {table_name} WHERE {id_column} = %s"
        
        mycursor.execute(query, (id_to_check,))
        
        if mycursor.fetchone() is None:
            print(f"Invalid {friendly_name} ID. Please enter a valid {friendly_name} ID.")
            id_to_check = input()
        else:
            check = False
            return id_to_check


def check_ship_fee(ship_fee:str):
    
    ship_fee = check_number_pos(ship_fee)

    return ship_fee


def yes_no_check():
    menu = True
    while menu == True:
        print("Please insert Y or N")
        response = input().upper()
        if response in ["Y","N"]:
            menu = False
            if response == "Y":
                return True
            else:
                return False
        else:
            print("ERROR: wrong input.")
    

def add_customer():

    print("Insert customers company name:")
    company = input()

    print("Insert customers first name:")
    f_name = input()

    print("Insert customers last name:")
    l_name = input()

    print("Insert customers e-mail address:")
    email = input()

    print("Insert customers job title:")
    job_title = input()

    print("Insert customers business phone:")
    b_phone = input()
    #ADD ERROR HANDELING?

    print("Insert customers home phone:")
    h_phone = input()
    #ADD ERROR HANDELING?

    print("Insert customers mobile phone:")
    m_phone = input()
    #ADD ERROR HANDELING?

    print("Insert customers Fax")
    fax = input()
    #ADD ERROR HANDELING?

    print("Insert customers address")
    address = input()

    print("Insert customers city")
    city = input()

    print("Insert customers state")
    state = input()
    #ADD ERROR HANDELING

    print("Insert customers zip code")
    zip_code = input()
    #ADD ERROR HANDELING

    print("Insert customers country")
    country = input()

    query = """
    INSERT INTO Customers
        (Company, FirstName, LastName, Email, JobTitle, BusinessPhone, 
         HomePhone, MobilePhone, Fax, Address, City, State, Zip, Country)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (company, f_name, l_name, email, job_title, b_phone, 
              h_phone, m_phone, fax, address, city, state, zip_code, country)

    mycursor.execute(query, values)
    db.commit()
    print(f"Successfully added customer: {f_name} {l_name}")


def add_order():

    #Check if product exists in Products Table

    #===================Get information from user===============================================================================================================================

    # Get Employee ID
    print("Insert your employee ID")
    emp_id = check_id_exists(input(), "Employees", "ID", "Employee")

    # Get Customer ID
    print("Insert the customer ID")
    cust_id = check_id_exists(input(), "Customers", "ID", "Customer")

    # Get product ID
    #Ask if ordering multiple products
    print("Will you be purchasing multiple products?")
    multiple_products = yes_no_check()

    if multiple_products:
        print("How many products will you be ordering?")
        num_products = check_number_pos(input())
        num_products = int(num_products)
    else:
        num_products = 1 

    # Get number of products for each product
    i = 0
    product_id = []
    for i in range(num_products):
        print(f"Insert the product {i+1} ID")
        prod_id_input = input()
        product_id.append(check_product_discontinued(prod_id_input))

    # Get product quantity
    product_quantity = []
    for i in range(num_products):
        print(f"How much of product {i+1} are you ordering?")
        product_quantity.append(input())
        product_quantity[i] = check_number_pos(product_quantity[i])


    # Get customer payment information
    pay_menu = True
    while pay_menu:
        print(f"Will the customer be paying today? (Y/N)")
        cust_paying = (input().upper())
        if cust_paying in ["Y", "N"]:
            if cust_paying == "N":
                payment_type = ('NULL')
                paid_date = ('NULL')
                break
            else:
                paid_date = (datetime.date.today())
                pay_menu = True
                while pay_menu:
                    print("How will the customer be paying?\n1.Check\n2.Cash\n3.Card")
                    paying_with = input()
                    if paying_with == "1":
                        payment_type = ("Check")
                        pay_menu = False
                    elif paying_with == "2":
                        payment_type = ("Cash")
                        pay_menu = False
                    elif paying_with == "3":
                        payment_type = ("Card")
                        pay_menu = False
                    else:
                        print("Invalid choice. Please insert 1, 2, or 3.")
                        time.sleep(1)
        else:
            print("Invalid choice. Please insert Y or N.")
            time.sleep(1)


    # Ask what Shipper ID will be used
    print("What Shipper ID will be used?")
    shipper_id = check_id_exists(input(), "Shippers", "ID", "Shipper")

    # Get shipping fee
    print("Please enter the shipping fee for the order.")
    ship_fee = input()
    ship_fee = check_ship_fee(ship_fee)

    
    #===========================================================================================================================================================================

    #====================Get information from DB================================================================================================================================

    result = []
    
    # For Unit Price: Get List Price from Products
    unit_price = []
    i=0
    for i in range(num_products):
        query = "SELECT ListPrice FROM Products WHERE ID = %s"
        mycursor.execute(query, (product_id[i],))

        result = mycursor.fetchone()
        unit_price.append(float(result[0]))

    # Get cust shipping information from Customers using Customer_ID
    
    query = """
        SELECT CONCAT(FirstName,' ',LastName), Address, City, State, Zip, Country 
        FROM Customers 
        WHERE ID = %s
    """
    mycursor.execute(query, (cust_id,))
    
    result = mycursor.fetchone()
    ship_name, ship_address, ship_city, ship_state, ship_zip, ship_country = result

    # Get Status ID from Orders Status

    if cust_paying =='Y':
        status_id = 2
    else:
        status_id = 1


    # Set tax rate to default
    tax_rate = '0'

    # Get order date
    order_date = datetime.datetime.now()
    order_date = order_date.replace(hour=0, minute=0, second=0, microsecond=0)

    # Get TransationType
    if cust_paying == 'Y':
        transaction_type = 1
    else:
        transaction_type = 3

    # Get SupplierID
    supplier_id = []
    i=0
    for i in range(num_products):
        query = "SELECT SupplierIDs FROM Products WHERE ID = %s"
        mycursor.execute(query, (product_id[i],))
        result = mycursor.fetchone()
        result = result[0]
        supplier_id.append(result)

    

    #===========================================================================================================================================================================


    #========================INSERT INTO DB=====================================================================================================================================

    # INSERT INTO Orders
    # You will first retrieve the OrderID value from Orders after inserting using SELECT_LAST_INSERT_ID(), then reuse in Order_Details
    query = """
    INSERT INTO Orders(EmployeeID,CustomerID,OrderDate,ShippedDate,ShipperID,ShipName,ShipAddress,ShipCity,ShipState,ShipZIP,ShipCountry,ShippingFee,Taxes,PaymentType,PaidDate,TaxRate,StatusID)
    VALUES(%s, %s, %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, '0.0000', %s, %s, '0', %s)
    """
    values = (emp_id, cust_id, order_date, shipper_id, ship_name, ship_address, ship_city, ship_state, ship_zip, ship_country, ship_fee, payment_type, paid_date, status_id)
    mycursor.execute(query, values)
    db.commit()

    mycursor.execute("SELECT LAST_INSERT_ID()")
    result = mycursor.fetchone()
    order_id = result[0]

    # INSERT INTO Inventory_Transactions and get Transaction_ID using last_insert_id() as Inventory ID
    inventory_id = []
    i=0
    for i in range(num_products):
        query = """
        INSERT INTO Inventory_Transactions(TransactionType,TransactionCreatedDate,TransactionModifiedDate,ProductID,Quantity)
        VALUES(%s, %s, %s, %s, %s)
        """
        values = (transaction_type, order_date, order_date, product_id[i], product_quantity[i])
        mycursor.execute(query, values)
        db.commit()

        mycursor.execute("SELECT LAST_INSERT_ID()")
        result = mycursor.fetchone()
        result = result[0]
        inventory_id.append(result)

    # INSERT INTO Purchase Orders and get Purchase_Order_ID using last_insert_id()
    purchase_order_id = []
    i=0
    for i in range(num_products):
        query = """
        INSERT INTO Purchase_Orders(SupplierID,CreatedBy,SubmittedDate,CreationDate,StatusID,ShippingFee,Taxes,PaymentAmount,PaymentMethod,SubmittedBy)
        VALUES(%s, %s, %s, %s, %s, %s, '0.0000', '0.0000', %s, %s)
        """
        values = (supplier_id[i], emp_id, order_date, order_date, status_id, ship_fee, payment_type, emp_id)
        mycursor.execute(query, values)
        db.commit()
    
        mycursor.execute("SELECT LAST_INSERT_ID()")
        result = mycursor.fetchone()
        result = result[0]
        purchase_order_id.append(result)
    

    # INSERT INTO Purchase Order Details
    i=0
    for i in range(num_products):
        query = """
        INSERT INTO Purchase_Order_Details(PurchaseOrderID,ProductID,Quantity,UnitCost,DateReceived,PostedToInventory,InventoryID)
        VALUES(%s, %s, %s, %s, %s, '1', %s)
        """
        values = (purchase_order_id[i], product_id[i], product_quantity[i], unit_price[i], order_date, inventory_id[i])
        mycursor.execute(query, values)
        db.commit()


    # INSERT INTO Order Details
    i=0
    for i in range(num_products):
        query = """
        INSERT INTO Order_Details(OrderID,ProductID,Quantity,UnitPrice,StatusID,PurchaseOrderID,InventoryID)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        """
        values = (order_id, product_id[i], product_quantity[i], unit_price[i], status_id, purchase_order_id[i], inventory_id[i])
        mycursor.execute(query, values)
        db.commit()


    # INSERT INTO Invoices
    i=0
    for i in range(num_products):
        query = """
        INSERT INTO Invoices(OrderID,InvoiceDate,Tax,Shipping,AmountDue)
        VALUES(%s, %s, '0.0000', %s, '0.0000')
        """
        values = (order_id, order_date, ship_fee)
        mycursor.execute(query, values)
        db.commit()

    #===========================================================================================================================================================================


def remove_order():
    print("Please enter the Order ID for the order you'd like to delete:")
    delete_order_id = check_id_exists(input(), "Orders", "OrderID", "Order")


    #DELETE from Invoices Table
    query = "DELETE FROM Invoices WHERE OrderID = %s"
    mycursor.execute(query, (delete_order_id,))
    db.commit()

    print("Order/s removed from Invoices Table.")
    time.sleep(1)

    # DELETE from Orders_Details
    query = "DELETE FROM Order_Details WHERE OrderID = %s"
    mycursor.execute(query, (delete_order_id,))
    db.commit()

    print("Order/s removed from Order_Details Table.")
    time.sleep(1)

    #DELETE from Purchase_Order_Details?

    # DELETE from Orders
    query = "DELETE FROM Orders WHERE OrderID = %s"
    mycursor.execute(query, (delete_order_id,))
    db.commit()

    print("Order/s removed from Orders Table.")
    time.sleep(1)

def ship_order():
    # Get ID (Order_Details ID) from user
    print("Please enter the Order Details ID of the order you'd like to ship.")
    id = check_id_exists(input(), "Order_Details", "ID", "Order Details")
    # FINISH order_id = check_order_id(order_id)

    # Select relative product from Order_Details using OrderID
    query = "SELECT ProductID FROM Order_Details WHERE ID = %s"
    mycursor.execute(query, (id,))
    result = mycursor.fetchone()
    product_id = result[0]

    # Get the order quantity of the relative order from Order_Details using OrderID
    query = "SELECT Quantity FROM Order_Details WHERE ID = %s"
    mycursor.execute(query, (id,))
    result = mycursor.fetchone()
    order_quantity = int(result[0])

    # Check if enough units are in stock to ship
    # To find units in stock of a product, use the InventoryTransactions table, 
    # find total quantity purchased and subtract quantities sold and on hold. 
    # If there are not enough units of any product in the order, the order cannot be shipped.

    query = """
    SELECT 
    %s, 
    (SUM(CASE WHEN TransactionType = '1' THEN Quantity ELSE 0 END) -
    SUM(CASE WHEN TransactionType = '2' THEN Quantity ELSE 0 END) -
    SUM(CASE WHEN TransactionType = '3' THEN Quantity ELSE 0 END)) AS AvailableQuantity
    FROM Inventory_Transactions
    WHERE ProductID = %s
    GROUP BY ProductID;
    """
    mycursor.execute(query, (product_id, product_id))

    result = mycursor.fetchone()
    available_quantity = int(result[1])
    
    if available_quantity < order_quantity:

        print("The available quantity is less than your order.")
        print("The order cannot be shipped.")
        time.sleep(2)

    elif available_quantity > order_quantity or available_quantity == order_quantity:

        print("Your order can be shipped!")
        time.sleep(1)

        # Get OrderID from Order_Details table using ID
        query = "SELECT OrderID FROM Order_Details WHERE ID = %s"
        mycursor.execute(query, (id,))
        result = mycursor.fetchone()
        order_id = result[0]

        # Get order date
        order_date = datetime.datetime.now()
        order_date = order_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # Insert Shipped Date into Orders Table using OrderID
        query = "UPDATE Orders SET ShippedDate = %s WHERE OrderID = %s"
        mycursor.execute(query, (order_date, order_id))
        db.commit()
        print("Updated Orders table with shipped date.")
        time.sleep(1)

        # For each product in the order, insert inventory transaction sold

        # THERE IS ACTUALLY NO WAY TO DO THIS CONSIDERING THAT All PREVIOUSLY INSERTED CustomerID's ARE NULL IN THE TABLE, if there is, let me know.



def print_pending_orders():
    print()
    # Print pending order list with NULL ShippedDate, print in order of order date

    mycursor.execute("""
    SELECT OrderID, OrderDate, CustomerID
    FROM Orders
    WHERE ShippedDate IS NULL
    ORDER BY OrderDate;
    """)

    pending_orders = mycursor.fetchall()
    print("==============================================================")
    for order in pending_orders:
        order_id, order_date, customer_id = order
        print(f"Order ID: {order_id}, Order Date: {order_date}, Customer ID: {customer_id}")
    print("==============================================================")
    time.sleep(3)

def more_options():
    print()

def display_menu():
    print(" _   _               _    _")
    print("| \ | | ___  ___   _| |_ | |    _       _  _               _")
    print("|  \| ||   ||  _\ |_   _|| |__ | |  _  | || |.=.____  ____| |")
    print("| |\  || | || |     | |  |  _ || |_| |_| || ||  __  ||  _   |")
    print("|_| \_||___||_|     |_|  |_||_||_________||_||_|  |_||______|")
    print("=======================")
    print("1. Add a customer")
    print("2. Add an order")
    print("3. Remove an order")
    print("4. Ship an order")
    print("5. Print pending orders")
    print("6. Exit")
    print("=======================")

def main():

    menu = True

    while menu:

        display_menu()
        choice = input("Please choose from options 1-6\n")

        if choice == "1":
            add_customer()
        elif choice == "2":
            add_order()
        elif choice == "3":
            remove_order()
        elif choice == "4":
            ship_order()
        elif choice == "5":
            print_pending_orders()
        elif choice == "6":
            print("Goodbye!")

            menu = False


        else:
            print("Invalid choice. Please enter a number between 1-6.\n")


if __name__ == "__main__":
    try:
        main()
    except mysql.connector.Error as err:
        print(f"A database error occurred: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if db.is_connected():
            mycursor.close()
            db.close()
            print("\nDatabase connection closed.")
