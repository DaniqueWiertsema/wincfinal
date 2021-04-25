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
    create_bought_file()
    create_sold_file()

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
report_inventory = report_subparsers.add_parser('inventory', help='inventory')
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

args=parser.parse_args()

def buy_item(product_name, buy_price, expiration_date, buy_date):
    with open('bought.csv', 'r+', newline='') as file:
        reader = csv.reader(file)
        next(reader) 
        find_buy_id = [0]
        for row in reader:
            bought_id = int(row[0])
            find_buy_id.append(bought_id)
        bought_id = max(find_buy_id)+1
        bought_item = csv.writer(file)
        bought_item.writerow([bought_id, product_name, date_bought, buy_price, expiration_date])

def sell_item(product_name, sell_price):  
    with open('sold.csv', 'r+', newline='') as sold_file:
        reader = csv.reader(sold_file)
        next(reader) 
        find_sold_id = [0] 
        sold_file.seek(0) 
        next(reader)
        for row in reader:
            sold_id = int(row[0])
            find_sold_id.append(sold_id) 
        sold_id = max(find_sold_id)+1 
        sold_item.writerow([sold_id, bought_id, date_sold, price])

def revenue(date_start, date_end): 
    with open('sold.csv', 'r+', newline='') as sold_file:
        reader = csv.reader(sold_file)
        next(reader)
        sold_values = [float(line[3]) for line in reader if date <= datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= date_end]
        total_revenue = sum(sold_values)
        return total_revenue

def all_sold_items(date_start, date_end): 
    with open('sold.csv', 'r+', newline='') as sold_file:
        reader = csv.reader(sold_file)
        next(reader)
        sold_items_id = [line[1] for line in reader if date <= datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= date_upper_limit]
        return sold_items_id

def profit(date_start, date_end):
    total_revenue = revenue_period(date_start, date_end)
    sold_items_id = find_sold_items(date_start, date_end)
    with open('bought.csv', newline='') as bought_file:
        reader = csv.reader(bought_file)
        next(reader) 
        buy_costs = [float(line[3]) for line in reader if line[0] in sold_items_id]
        total_costs = sum(buy_costs)
        total_profit = total_revenue - total_costs
        return total_profit

if __name__ == '__main__':
    startup()
    if args.command == "buy" :
        buy_item(args.product_name, args.buy_price, args.expiration_date, args.buy_date)
        print('check')
    if args.command == 'sell':
        sell_item(args.product_name, args.sell_price)
        print('check')
    if args.command == 'inventory':
        check_inventory(date)
    if args.command == 'revenue':
        check_revenue(date)
    if args.command == 'profit':
        check_profit(date)
