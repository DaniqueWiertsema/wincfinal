#imports
import argparse
import csv
import sys
import pandas as pd
import os
from os import path
import datetime
from datetime import date, datetime, timedelta
from datetime import date as datum
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

#parsers
parser = argparse.ArgumentParser(description='keep track of my store', formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)
subparsers = parser.add_subparsers(dest='command')

buy_parser = subparsers.add_parser('buy', help='registers bought products')
buy_parser.add_argument('--product_name', metavar='\b', required = True, type=str, help='product name')
buy_parser.add_argument('--buy_price', metavar='\b', required = True, type=float, help='price')
buy_parser.add_argument('--expiration_date', metavar='\b', required = True, type=str, help='expiration date in YYYY-mm-dd')

sell_parser = subparsers.add_parser('sell', help='registers sold products')
sell_parser.add_argument('--product_name', metavar='\b', type=str, help='product name')
sell_parser.add_argument('--sell_price', metavar='\b', type=float, help='price')

date_parser = subparsers.add_parser('advance_time', help='advances date by x days')
date_parser.add_argument('--days', help='type number of days to advance date with')

report_parser = subparsers.add_parser('report', help='creates a report')    
report_subparsers = report_parser.add_subparsers(dest='command', help='type of report')
report_revenue = report_subparsers.add_parser('revenue', help='revenue')
report_profit = report_subparsers.add_parser('profit', help='profit')

report_revenue.add_argument('--today', action='store_true', help='shows todays revenue')
report_revenue.add_argument('--yesterday', action='store_true', help='shows yesterdays revenue')
report_revenue.add_argument('--date', type=str, help='shows revenue from date YYYY-mm-dd uptil today')

report_profit.add_argument('--today', action='store_true', help='shows todays profit')
report_profit.add_argument('--yesterday', action='store_true', help='shows yesterdays profit')
report_profit.add_argument('--date', type=str, help='shows profit from date YYYY-mm-dd uptil today') 

plot_parser = subparsers.add_parser('plot_revenue', help='creates a visualization of revenue')
plot_parser.add_argument('--date', type=str, help='shows revenue per day between date YYYY-mm-dd uptil today')

export_parser = subparsers.add_parser('export_to_excel', help = 'export your report to xlsx')
export_parser.add_argument('--sold', action='store_true', help='sold items')
export_parser.add_argument('--bought', action='store_true', help = 'bought items')

report_inventory_parser = subparsers.add_parser('report_inventory', help = 'report current amount in stock of chosen product')
report_inventory_parser.add_argument('--all_products', action = 'store_true', help = 'shows current stock (all products)')
report_inventory_parser.add_argument('--product', metavar='\b', type=str, help = 'shows current amount of chosen product')

args=parser.parse_args()

#functions
def startup():
    create_date_file()
    sold_header = ['id', 'bought_id', 'product_name', 'sell_date', 'sell_price']
    bought_header = ['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date']
    inventory_header = ['bought_id', 'product_name', 'buy_date', 'buy_price', 'expiration_date']
    create_file('sold.csv', sold_header)
    create_file('bought.csv', bought_header)
    create_file('inventory.csv', inventory_header)

def create_date_file():
    if path.exists('date.txt') == False:
        date = datum.today()
        file = open('date.txt', 'w')
        file.write(datetime.strptime(date))

def create_file(file_name, headers):
    if path.exists(file_name) == False:
        with open(file_name, 'w', newline='') as csvfile:
            creator = csv.writer(csvfile)
            creator.writerow(headers)

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
    with open('inventory.csv', 'r+', newline='') as file:
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

def sell_item(product_name, sell_price): #function for selling items
    sell_date = datum.today()
    with open('sold.csv', 'r+', newline='') as sold_file: #creates unique sold id
        reader = csv.reader(sold_file)
        next(reader) 
        find_sold_id = [0] 
        sold_file.seek(0) 
        next(reader)
        for row in reader:
            sold_id = int(row[0])
            find_sold_id.append(sold_id) 
        sold_id = max(find_sold_id)+1

    inv_df = pd.read_csv("inventory.csv", sep=',')
    available_products = inv_df[inv_df['product_name'] == product_name]
    if available_products.empty:
        print('Item not available, consider buying it ;)')
    else:
        available_products = available_products.reset_index()
        bought_id = available_products['bought_id'].loc[0]
        inv_df_deleted = inv_df[inv_df['bought_id'] != bought_id]
        inv_df_deleted.to_csv("inventory.csv", sep=',', index=False)

        with open('sold.csv', 'a', newline='') as sold_file:
            sold_item = csv.writer(sold_file)
            sold_item.writerow([sold_id, bought_id, product_name, sell_date, sell_price])
            print(f'{product_name} sold and added to sold.csv')

def advance_time(x): #set the date the applicaation perceives as 'today'
    datenow = datum.today()
    days_to_advance = int(x) 
    future = timedelta(days=days_to_advance)
    total = str(datenow + future)
    file = open('date.txt', 'w')
    file.write(total)
    file.close()
    print(f'The date is advanced with {x} days. The new date is {total}.')

def period(time): #makes it possible to report for today, yesterday and a period uptil today
    datenow = datum.today()
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
    sold_df = pd.read_csv('sold.csv', sep=',')
    sold_df['sell_date']=pd.to_datetime(sold_df['sell_date']).dt.date
    df_revenue = sold_df[(sold_df['sell_date'] <= datenow) & (sold_df['sell_date'] >= date_end)]
    revenue = df_revenue['sell_price'].sum()
    print(f' The revenue between {date_end} and {datenow} is ???{revenue}.') 
    sold_items_id = df_revenue.bought_id.unique()
    return revenue, df_revenue, sold_items_id 

def visualize_revenue(datenow, date_end): #creates bar chart of sales per day for given period
    sold_df = pd.read_csv('sold.csv', sep=',')
    sold_df['sell_date']=pd.to_datetime(sold_df['sell_date']).dt.date
    all_sold_items_df = sold_df[(sold_df['sell_date'] <= datenow) & (sold_df['sell_date'] >= date_end)]
    sum_per_day = all_sold_items_df.groupby(by=['sell_date'], as_index=False).sum()  
    colors = ['red', 'blue']
    plt.bar(sum_per_day['sell_date'], sum_per_day['sell_price'], color = colors)
    #lay-out options below
    plt.title(f'Revenue per day between {date_end} and {datenow}')
    plt.xlabel('Date')
    plt.ylabel('Revenue in ???')
    plt.grid(True)
    ax = plt.subplot(111)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b, %d'))
    plt.show()

def profit(datenow, date_end):
    revenue_period = revenue(datenow, date_end)
    sold_items_ids = revenue_period[2]
    revenue_for_profit = revenue_period[0]
    df_bought = pd.read_csv('bought.csv', sep=',')
    cost_list = []
    for sold_id in sold_items_ids:
        temp_df = df_bought[df_bought['id']== sold_id]
        temp_cost = temp_df['buy_price'].sum()
        cost_list.append(temp_cost)
    total_costs = sum(cost_list)
    profit = revenue_for_profit - total_costs
    print(f'The profit between {date_end} and {datenow} is ???{profit}.')
    return profit    

def print_to_excel(report_type): #function to export files to Excel-format
    output_date = datum.today()
    current_dir = os.getcwd()
    print(current_dir)
    if report_type == 'sold':
        sold_df = pd.read_csv('sold.csv', sep=',')
        output_name = (f'Sales_up_to_{output_date}.xlsx')
        sold_df.to_excel(output_name, index=False)
    if report_type == 'bought':
        bought_df = pd.read_csv('bought.csv', sep=',')
        output_name = (f'Bought_until_{output_date}.xlsx')
        bought_df.to_excel(output_name, index=False)
    print(f'Output printed to xlsx file: {output_name}')

def report_inventory(products):
    output_date = datum.today()
    if products == 'all_products':
        output_name = "all products"
        inv_df = pd.read_csv("inventory.csv", sep=',')
        df_to_group = inv_df[:]
        counted_df = df_to_group.groupby(by=['product_name']).count()
        counted_df = counted_df.reset_index()
        counted_df['no._products'] = counted_df['bought_id']
        counted_df = counted_df[['product_name', 'no._products']]
        counted_df.to_csv(f"Inventory report of {output_name}, {output_date}.csv", sep=',', index=False)
    else:
        output_name = products
        inv_df = pd.read_csv("inventory.csv", sep=',')
        available_products = inv_df[inv_df['product_name'] == products]
        if available_products.empty:
            print('Item not available, no report can be made')
        else:
            counted_df = available_products.groupby(['product_name']).count()
            counted_df = counted_df.reset_index()
            counted_df['no._products'] = counted_df['bought_id']
            counted_df = counted_df[['product_name', 'no._products']]
            counted_df.to_csv(f"Inventory report of {output_name}, {output_date}.csv", sep=',', index=False)


if __name__ == '__main__':
    startup()
    if args.command == "buy" :
        buy_item(args.product_name, args.buy_price, args.expiration_date)
    if args.command == 'sell':
        sell_item(args.product_name, args.sell_price)
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
    if args.command == 'plot_revenue':
        datenow, date_end = period(args.date)
        visualize_revenue(datenow, date_end)
    elif args.command == 'export_to_excel':
        if args.sold == True : 
            print_to_excel('sold')
        if args.bought == True : 
            print_to_excel('bought')
    elif args.command == 'report_inventory':
        if args.all_products == True :
            report_inventory("all_products")
        elif args.product:
            report_inventory(args.product)


