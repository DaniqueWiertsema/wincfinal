# Imports
import argparse
import csv
import sys
import pandas as pd
import os
from os import path
import datetime
from datetime import date, datetime, timedelta

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.
def main():
    pass

#parsers
parser = argparse.ArgumentParser(description='keep track of my store', formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)
subparsers = parser.add_subparsers(dest='command')

buy_parser = subparsers.add_parser('buy', help='registers bought products')
buy_parser.add_argument('--product_name', metavar='\b', required = True, type=str, help='product name')
buy_parser.add_argument('--buy_price', metavar='\b', required = True, type=float, help='price')
buy_parser.add_argument('--expiration_date', metavar='\b', required = True, type=str, help='expiration date in YYYY-MM-DD')

sell_parser = subparsers.add_parser('sell', help='registers sold products')
sell_parser.add_argument('--product_name', metavar='\b', type=str, help='product name')
sell_parser.add_argument('--sell_price', metavar='\b', type=float, help='price')
sell_parser.add_argument('--sell_date', metavar='\b', type=str, help='date item was sold in YYYY-MM-DD')

date_parser = subparsers.add_parser('advance_time', help='advances date by x days')
date_parser.add_argument('--days', help='type number of days to advance date with')

report_parser = subparsers.add_parser('report', help='creates a report')    
report_subparsers = report_parser.add_subparsers(dest='command', help='type of report')
report_inventory = report_subparsers.add_parser('inventory', help='inventory')
report_revenue = report_subparsers.add_parser('revenue', help='revenue')
report_profit = report_subparsers.add_parser('profit', help='profit')

report_revenue.add_argument('--today', action='store_true', help='shows todays revenue')
report_revenue.add_argument('--yesterday', action='store_true', help='shows yesterdays revenue')
report_revenue.add_argument('--date', type=str, help='shows revenue from date YYYY-mm-dd uptil today')

report_profit.add_argument('--today', action='store_true', help='shows todays profit')
report_profit.add_argument('--yesterday', action='store_true', help='shows yesterdays profit')
report_profit.add_argument('--date', type=str, help='shows profit on date YYYY-mm-dd') 

args=parser.parse_args()

#functions
def startup():
    create_date_file()
    create_bought_file()
    create_sold_file()

def create_date_file(): #creates date file
    if path.exists('date.txt') == False :
        date = date.today()
        file = open('date.txt', 'w')
        file.write(date)

def create_bought_file(): #create oversight of items bought
    if path.exists('bought.csv') == False:
        with open('bought.csv', 'w', newline='') as csvfile:
            bought_creator = csv.writer(csvfile)
            bought_creator.writerow(['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date'])

def create_sold_file(): #create oversight of items sold
    if path.exists('sold.csv') == False:
        with open('sold.csv', 'w', newline='') as csvfile:
            sold_creator = csv.writer(csvfile)
            sold_creator.writerow(['id', 'bought_id', 'product_name', 'sell_date', 'sell_price'])

def buy_item(product_name, buy_price, expiration_date): #function for buying items
    buy_date = date.today()
    with open('bought.csv', 'r+', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        find_buy_id = [0]
        for row in reader:
            bought_id = int(row[0])
            find_buy_id.append(bought_id)
        bought_id = max(find_buy_id)+1
        bought_item = csv.writer(file)
        bought_item.writerow([bought_id, product_name, buy_date, buy_price, expiration_date])
        print(f'{product_name} bought and added to bought.csv')

def sell_item(product_name, sell_price, sell_date): #function for selling items
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
    with open('bought.csv', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        stock = [line[0] for line in bought_reader if line[1] == product_name]
        if stock:
            bought_id = stock[0]
            with open('sold.csv', 'a', newline='') as sold_file:
                sold_item = csv.writer(sold_file)
                sold_item.writerow([sold_id, bought_id, product_name, sell_date, sell_price])
                print(f'{product_name} sold and added to sold.csv')
        else:
            print('Item not available, consider buying it ;)')

def advance_time(x): #helps to set times
    datenow = date.today()
    days_to_advance = int(x) 
    future = timedelta(days=days_to_advance)
    total = str(datenow + future)
    file = open('date.txt', 'w')
    file.write(total)
    file.close()
    print(f'The date is advanced with {x} days. The new date is {total} date.')

def period(time): #makes it possible to report for today, yesterday and a period uptil today
    datenow = date.today()
    resolution = time.count('-') #checks if period is formatted correctly (YYYY-mm-dd)
    if time == 'today':
        date_end = datenow
        return datenow, date_end
    if time == 'yesterday':
        yesterday = datenow + timedelta(days=-1)
        datenow = yesterday
        date_end = yesterday
        return datenow, date_end
    if resolution == 2: 
        specified_period = datetime.strptime(time, "%Y-%m-%d").date()
        date_end = specified_period
        return datenow, date_end
    else:
         print('Input does not meet requirements, use help function')

def revenue(datenow, date_end):
    path = r'C:\Users\d.wiertsema\sold.csv'
    sold_df = pd.read_csv(path, sep=',')
    sold_df['sell_date']=pd.to_datetime(sold_df['sell_date']).dt.date
    df_revenue = sold_df[(sold_df['sell_date'] <= datenow) & (sold_df['sell_date'] >= date_end)]
    revenue = df_revenue['sell_price'].sum()
    print(f' The revenue between {date_end} and {datenow} is €{revenue}.') 
    sold_items_id = df_revenue.bought_id.unique()
    return revenue, df_revenue, sold_items_id #list of all sold items in given period

def profit(datenow, date_end):
    revenue_period = revenue(datenow, date_end)
    sold_items_ids = revenue_period[2]
    revenue_for_profit = revenue_period[0]
    path_bought = r'C:\Users\d.wiertsema\bought.csv'
    df_bought = pd.read_csv(path_bought, sep=',')
    cost_list = []
    for sold_id in sold_items_ids:
        temp_df = df_bought[df_bought['id']== sold_id]
        temp_cost = temp_df['buy_price'].sum()
        cost_list.append(temp_cost)
    total_costs = sum(cost_list)
    profit = revenue_for_profit - total_costs
    print(f'The profit between {date_end} and {datenow} is €{profit}.')
    return profit
     
if __name__ == '__main__':
    startup()
    if args.command == "buy" :
        buy_item(args.product_name, args.buy_price, args.expiration_date)
    if args.command == 'sell':
        sell_item(args.product_name, args.sell_price, args.sell_date)
    if args.command == 'advance_time':
        advance_time(args.days)
    if args.command == 'revenue':
        if args.today == True :
            datenow, date_end = period('today')
            revenue(datenow, date_end)
        elif args.yesterday == True : 
            datenow, date_end = period('yesterday') 
            revenue(datenow, date_end)
        elif args.date:
            datenow, date_end = period(args.date)
            revenue(datenow, date_end)
    if args.command == 'profit':
        if args.today == True :
            datenow, date_end = period('today')
            profit(datenow, date_end)
        elif args.yesterday == True : 
            datenow, date_end = period('yesterday')
            profit(datenow, date_end)
        elif args.date : 
            datenow, date_end = period (args.date)
            profit(datenow, date_end)