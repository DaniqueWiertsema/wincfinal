# Imports
import argparse
import csv
import sys
from os import path
import datetime
from datetime import date, datetime, timedelta

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.
def main():
    pass

# Date variables
now = datetime.now()
today = datetime.today().strftime("%Y-%m-%d")
yesterday = date.today() - timedelta(days=1)
tomorrow = date.today() + timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")
tomorrow_str = tomorrow.strftime("%Y-%m-%d")

def startup():
    create_date_file()
    create_bought_file()
    create_sold_file()

# Function to create a file with the current date as filename.
def create_date_file(): 
    if path.exists('date.txt') == False:
        date = str(datetime.today())
        file = open('date.txt', 'w')
        file.write(date)
        file.close()

def create_bought_file():
    if path.exists('bought.csv') == False:
        with open('bought.csv', 'w', newline='') as csvfile:
            bought_creator = csv.writer(csvfile)
            bought_creator.writerow(['id', 'product_name', 'date_buy', 'price_buy', 'expiration_date'])

def create_sold_file():
    if path.exists('sold.csv') == False:
        with open('sold.csv', 'w', newline='') as csvfile:
            sold_creator = csv.writer(csvfile)
            sold_creator.writerow(['id', 'bought_id', 'date_sell', 'price_sell'])


parser = argparse.ArgumentParser(description='keep track of my store', formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
subparsers = parser.add_subparsers(dest='command')

buy_parser = subparsers.add_parser('buy', help='registers bought products')
buy_parser.add_argument('--productname', metavar='\b', required = True, type=str, help='product name')
buy_parser.add_argument('--buyprice', metavar='\b', required = True, type=float, help='price')
buy_parser.add_argument('--experationdate', metavar='\b', required = True, type=str, help='expiration date in  YYYY-MM-DD')

sell_parser = subparsers.add_parser('sell', help='registers sold products')
sell_parser.add_argument('--product-name', metavar='\b', type=str, help='product name')
sell_parser.add_argument('--price', metavar='\b', type=float, help='price')

report_parser = subparsers.add_parser('report', help='creates a report')    
report_subparsers = report_parser.add_subparsers(dest='command', help='type of report')
report_inventory = report_subparsers.add_parser('inventory', help=' inventory')
report_revenue = report_subparsers.add_parser('revenue', help='revenue')
report_profit = report_subparsers.add_parser('profit', help='profit')

report_inventory.add_argument('--now', action='store_true', help='shows current inventory')
report_inventory.add_argument('--yesterday', action='store_true', help='shows yesterdays inventory')
report_inventory.add_argument('--date', type=str, help='shows inventory on date YYYY-mm-dd')

report_revenue.add_argument('--today', action='store_true', help='shows todays revenue')
report_revenue.add_argument('--yesterday', action='store_true', help='shows yesterdays revenue')
report_revenue.add_argument('--date', type=str, help='shows revenue on date YYYY-mm-dd')

report_profit.add_argument('--today', action='store_true', help='shows todays profit')
report_profit.add_argument('--yesterday', action='store_true', help='shows yesterdays profit')
report_profit.add_argument('--date', type=str, help='shows profit on date YYYY-mm-dd') 

import_json_parser = subparsers.add_parser('importjson', help='import old stock from a json file')
import_json_parser.add_argument('--path', help='path to json file')

export_json_parser = subparsers.add_parser('exportjson', help='export current file to json file')
export_json_parser.add_argument('--reporttype', help='export inventory, revenue, profit, bought or sales')

graph_parser = subparsers.add_parser('showgraph', help='show a graph with current data')
graph_parser.add_argument('--reporttype', help='export inventory, revenue, profit, bought or sales')

args=parser.parse_args()

#The main action for buying a product. Requires a name, price, expiration date and date of purchase
#Generates a new ID based on the last know ID and stores all values in a csv file.
def buy_item(product_name, buy_price, expiration_date, buy_date):
    product_name = product_name.lower()
    with open('bought.csv', 'r+', newline='') as file:
        reader = csv.reader(file)
        next(reader) 
        find_buy_id = [0]
        for row in reader:
            bought_id = int(row[0])
            find_buy_id.append(bought_id)
        bought_id = max(find_buy_id)+1
        if buy_date == 'today':
            date_bought = get_date()
        else:
            date_bought = buy_date
        bought_item = csv.writer(file)
        bought_item.writerow([bought_id, product_name, date_bought, buy_price, expiration_date])

#The main action for selling a product. Requires a name and price and stores these values with the Buy-ID in a csv file. 
def sell_item(product_name, sell_price):  
    date = get_date()
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader) 
        sold_items_list = [line[1] for line in sold_reader] 
        find_sold_id = [0] 
        sold_file.seek(0) 
        next(sold_reader)
        for row in sold_reader:
            sold_id = int(row[0])
            find_sold_id.append(sold_id) 
        sold_id = max(find_sold_id)+1 #Determine the new sell_ID by taking the highest currently present ID and adding +1
    with open('bought.csv', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        next(bought_reader)
        #Now the function checks for availability of the item: were there more products with this name bought than sold, and did these products not expire?
        stock = [line[0] for line in bought_reader if line[1] == product_name and datetime.datetime.strptime(line[4], "%Y-%m-%d").date() >= date and line[0] not in sold_items_list] #Creates a list of all items with that product name that are not expired nor sold
        if stock:
            bought_id = stock[0]
            with open('sold.csv', 'a', newline='') as sold_file:
                sold_item = csv.writer(sold_file)
                sold_item.writerow([sold_id, bought_id, date, sell_price])
        else:
            print('Item not in stock')

#Funtion to check the inventory on a given moment, using one argument: the date that is requested.
#Result is stored as a separate csv file with name "Inventory {date}" and also printed on the command line
def check_inventory(time):
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader) 
        sold_items_list = [line[1] for line in sold_reader if datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= time] #Creates a list of ids for all items sold
    with open('bought.csv', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        next(bought_reader) 
        stock = [[line[1].lower(), line[3], line[4]] for line in bought_reader if datetime.datetime.strptime(line[4], "%Y-%m-%d").date() > time and line[0] not in sold_items_list and datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= time] #Creates a list of all items that are not expired nor sold
        unique_stock =[]
        for i in stock:
            if i not in unique_stock:
                unique_stock.append(i)
                unique_stock = sorted(unique_stock)
        fields = ['Product name', 'Count', 'Buy Price', 'Expiration Date']
        with open(f'Inventory {time}.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(unique_stock)
        inventory = f'Inventory saved as Inventory {time}.csv \nProduct name \tCount \tBuy Price \tExpiration Date' #eindresultaat opmaken
        for row in unique_stock:
            inventory = inventory + f'\n{row[0]} \t\t{stock.count(row)} \t{row[1]} \t\t{row[2]}'
        print(inventory)
        return inventory

#The main function to determine the revenue in a given period. Either one day, in which case both required
#arguments are equal, or a given period with a start and end date.
#Function returns the total revenue to the function that called it.
def revenue_period(date, date_upper_limit): 
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader)
        sold_values = [float(line[3]) for line in sold_reader if date <= datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= date_upper_limit]
        total_revenue = sum(sold_values)
        return total_revenue

#Helper function to find all find the Buy_ID's of products sold in a certain period.
def find_sold_items(date, date_upper_limit): 
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader)
        sold_items_id = [line[1] for line in sold_reader if date <= datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= date_upper_limit]
        return sold_items_id

#The main function to determine the profit in a given period. Either one day, in which case both required
#arguments are equal, or a given period with a start and end date.Profit is determined by comparing the
#revenue in that period to the costs of buying all products that are sold in that period.
#Function returns the total profit to the function that called it.
def profit(date, date_upper_limit):
    total_revenue = revenue_period(date, date_upper_limit)
    sold_items_id = find_sold_items(date, date_upper_limit)
    with open('bought.csv', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        next(bought_reader) 
        costs = [float(line[3]) for line in bought_reader if line[0] in sold_items_id]
        total_costs = sum(costs)
        total_profit = total_revenue - total_costs
        return total_profit

#Helper function to identify the right time period to be used with the various functions, based on
#input from either the command line or the user interface
def determine_period(time):
    date = get_date()
    date_upper_limit = date
    if time == 'today' or time == 'now':
        date_upper_limit = get_date()
    elif time == 'yesterday':
        date = date + datetime.timedelta(days = -1)
        date_upper_limit = date
    else: #following lines based on YYYY-mm-dd format, as required.
        resolution = time.count('-') #Check if either a year, year-month or year-month-day is specified
        if resolution == 2:  #for year-month-day
            date = datetime.datetime.strptime(time, "%Y-%m-%d").date()
            date_upper_limit = date
        elif resolution == 1: #for year-month
            date = datetime.datetime.strptime(time, "%Y-%m").date()
            date_upper_limit = date
            date_month = date.strftime("%B")
#determine last day of the month, taking into account
#possible 28 (feb non-leap year) 29 (feb leap year), 30 of 31 day possibilities.
            for i in range(31): 
                date_upper_limit = date_upper_limit + datetime.timedelta(days = +1)
                if date_upper_limit.month > date.month:
                    date_upper_limit = date_upper_limit + datetime.timedelta(days = -1)
                    break
        elif resolution == 0 and len(time) == 4: #if only a year is given
            date = datetime.datetime.strptime(time, "%Y").date()
            date_upper_limit = datetime.date(date.year, 12, 31)
        elif resolution == 4 and len(time) == 21: #if a certain period is given in format YYYY-mm-dd-YYY-mm-dd
            date = datetime.datetime.strptime(time[0:9], "%Y").date()
            date_upper_limit = datetime.datetime.strptime(time[10:21], "%Y").date()
    return date, date_upper_limit

if __name__ == '__main__':
    startup()
    if args.command == "buy" :
        buy_item(args.product_name, args.buy_price, args.expiration_date, args.buy_date)
        print('check')
    if args.command == 'sell':
        sell_item(args.product_name, args.sell_price)
        print('check')
    if args.command == 'inventory':
        if args.now == True:
            date, date_upper_limit = determine_period('now')
        elif args.yesterday == True:
            date, date_upper_limit = determine_period('yesterday')
        elif args.date:
            date, date_upper_limit = determine_period(args.date)
        check_inventory(date)
    if args.command == 'revenue':
        if args.today == True:          
            date, date_upper_limit = determine_period('today')
            print(f'Today\'s revenue so far: {revenue_period(date, date_upper_limit)}')
        elif args.yesterday == True:
            date, date_upper_limit = determine_period('yesterday')
            print(f'Yesterday\'s revenue: {revenue_period(date, date_upper_limit)}')
        elif args.date:
            date, date_upper_limit = determine_period(args.date)
            if args.date.count('-') == 2:
                date_month = date.strftime("%B")
                print(f'Revenue from {date.day} {date_month} {date.year}: {revenue_period(date, date_upper_limit)}')
            elif args.date.count('-') == 1:
                date_month = date.strftime("%B")
                print(f'Revenue from {date_month} {date.year}: {revenue_period(date, date_upper_limit)}')
            elif args.date.count('-') == 0 and len(args.date) == 4:
                print(f'Revenue from {date.year}: {revenue_period(date, date_upper_limit)}')
        elif args.period:
            date, date_upper_limit = determine_period(args.period)
            print(f'Revenue from {args.period}: {revenue_period(date, date_upper_limit)}')
    if args.command == 'profit':
        if args.today == True:          
            date, date_upper_limit = determine_period('today')
            print(f'Today\'s profit so far: {profit(date, date_upper_limit)}')
        elif args.yesterday == True:
            date, date_upper_limit = determine_period('yesterday')
            print(f'Yesterday\'s profit: {profit(date, date_upper_limit)}')
        elif args.date:
            date, date_upper_limit = determine_period(args.date)
            if args.date.count('-') == 2:
                date_month = date.strftime("%B")
                print(f'Profit from {date.day} {date_month} {date.year}: {profit(date, date_upper_limit)}')
            elif args.date.count('-') == 1:
                date_month = date.strftime("%B")
                print(f'Profit from {date_month} {date.year}: {profit(date, date_upper_limit)}')
            elif args.date.count('-') == 0 and len(args.date) == 4:
                print(f'Profit from {date.year}: {profit(date, date_upper_limit)}')
        elif args.period:
            date, date_upper_limit = determine_period(args.period)
            print(f'Profit from {args.period}: {profit(date, date_upper_limit)}')


print(now)
