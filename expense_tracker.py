#sketch of my expense tracker

#import modules
import psycopg2
import pandas as pd
import numpy as np
import pandas.io.sql as psql
import matplotlib.pyplot as plt
import matplotlib.dates
import seaborn as sns
from datetime import datetime

#create database and connect to it:
conn = psycopg2.connect(
    host = "localhost",
    database = "expense_base",
    user = "postgres",
    password = ?????,
    port = "5433"
)

cur = conn.cursor()

#creating table with appropriate fields:
cur.execute("CREATE TABLE expenses (type text, cost float, trans_date date, month_sum float)")
conn.commit()

#creating a class that allows to define expenditure objects:
class Expense:
    def __init__(self, expense_type, cost, trans_date = datetime.now().date()):
        self.expense_type = expense_type
        self.cost = cost
        self.trans_date = trans_date

    def change_type(self, expense_type):
        self.expense_type = expense_type

    def change_cost(self, cost):
        self.cost = cost

    def change_date(self, trans_date):
        self.trans_date = trans_date

    def __str__(self):
        return f'Your last expense type: {self.expense_type}/ Cost: {self.cost} (PLN). / Transaction date: {self.trans_date}'

#function that allows to load the expense to database
def load_expense(expense):
    month_sum = expense.cost
    cur.execute("select expense_type, cost, trans_date from expenses")
    data = cur.fetchall()
    trans_months = []
    expense_types = set()
    for i in data:
        trans_months.append(i[2].month)
        expense_types.add(i[0])
        if expense.trans_date.month == i[2].month and expense.expense_type == i[0]:
            month_sum += i[1]
    cur.execute("insert into expenses (expense_type,cost,trans_date,month_sum) values (%s,%s,%s,%s)", (expense.expense_type, expense.cost, expense.trans_date, month_sum))
    #if it is new expense in current month add also expense "ZERO" with 0 cost, and 0 month_sum
    print(expense_types)
    if expense.trans_date.month not in trans_months:
        for i in expense_types:
            cur.execute("insert into expenses (expense_type,cost,trans_date,month_sum) values (%s,%s,%s,%s)",
                    (i,0,datetime.strptime(str(expense.trans_date.year)+"-"+str(expense.trans_date.month)+"-"+'01',"%Y-%m-%d"),0))
        #cur.execute("insert into expenses (expense_type,cost,trans_date,month_sum) values (%s,%s,%s,%s)",
                    #('entertainment',0,datetime.strptime(str(expense.trans_date.year)+"-"+str(expense.trans_date.month)+"-"+'01',"%Y-%m-%d"),0))
    conn.commit()

#function that allows you to select an expense for which you want to set a limit:
def choose_limit():
    df = psql.read_sql('select * from expenses', conn)
    options = {option for option in df['expense_type']}
    print("Type of expenses:")
    for option in options:
        print(option)
    limit_type = input("Choose type of expenses for which you would like to set limit: ")
    return limit_type

#function that allows you to set limit:
def set_limit():
    limit = int(input("Set limit: "))
    return limit

#define a dictionary that holds months
months = {1: "January",
          2: "February",
          3: "March",
          4: "April",
          5: "May",
          6: "June",
          7: "July",
          8: "August",
          9: "September",
          10: "October",
          11: "November",
          12: "December"}

#function that allows to plot data - MONTHLY SUM
def plot_monthly_sum():  
    options = {option for option in df['expense_type']}
    print("Type of expenses:")
    for option in options:
        print (option)
    your_choose = input("choose whether you want to display the monthly sum of all expenses ('all') or individual expenses listed above:")
    if your_choose == 'all':
        for key, value in months.items():
            print(key, "-", value)
        month = int(input("Choose the month for which you want to see the chart: "))
        df = psql.read_sql("select * from expenses where date_part('month',expenses.trans_date) = " + str(month), conn)
        x=df['trans_date']
        y=df['month_sum']
        sns.set_style('whitegrid')
        sns.lineplot(x,y,hue=df['expense_type'],style=df['expense_type'],markers=True,dashes=False)
        plt.show()
    elif your_choose != 'all' and your_choose not in options:
        print ('There is no such expense.')
        plot_monthly_sum()
    else:
        for key, value in months.items():
            print(key, "-", value)
        month = int(input("Select a month for which you want to see the chart: "))
        df = psql.read_sql("select * from expenses where expense_type like"+"'"+your_choose+"'"+" and date_part('month',expenses.trans_date) = "+str(month)+" order by date_part('day',trans_date)",conn)
        if your_choose == LIMIT_TYPE:
            plt.hlines(y=LIMIT, xmin=df['trans_date'].iloc[0], xmax=df['trans_date'].iloc[-1], color='r', linestyle='-', label = 'monthly limit')
            x = df['trans_date']
            y = df['month_sum']
            sns.set_style('whitegrid')
            sns.lineplot(x, y, marker='o')
            plt.show()
        else:
            x=df['trans_date']
            y=df['month_sum']
            sns.set_style('whitegrid')
            sns.lineplot(x,y,marker='o')
            plt.show()

#function that allows to plot data - SPECIFIC EXPENSES ON SPECIFIC DAYS in the selected month (or whole year but not recomended):
def plot_specific():
    cur.execute("select expense_type from expenses")
    data = cur.fetchall()
    types = {i[0] for i in data}
    print("Type of Expenses:")
    for i in types:
        print (i)
    choose_type = ""
    while choose_type not in types:
        choose_type = input("Choose type of expenses to plot: ")
    for key, value in months.items():
        print(key, "-", value)
    month_or_all = input("Select a month for which you want to see the chart or plot all(0):  ")
    if month_or_all == '0':
        df = psql.read_sql('select * from expenses where expense_type like '+"'"+choose_type+"'"+'and cost != 0', conn)
        x=df['trans_date']
        y=df['cost']
        sns.set_style('whitegrid')
        sns.lineplot(x, y, marker="o").set_title(choose_type)
        plt.show()
    elif month_or_all.isnumeric() and month_or_all != '0' and int(month_or_all) <= 12:
        df = psql.read_sql('select * from expenses where expense_type like '+"'"+choose_type+"'"+ " and date_part('month',trans_date) = "+month_or_all,conn)
        x = df['trans_date']
        y = df['cost']
        sns.set_style('whitegrid')
        sns.lineplot(x, y, marker="o").set_title(choose_type)
        plt.show()
    else:
        print ("Wrong input")
        plot_specific()

#function that plot plotbar with total sum of expenses
def plot_month_bar():
    def answer():
        your_choose = input("Choose whether you would like to plot monthly barplot which shows the total costs of all types of expenses or separate: (all/separate)")
        return your_choose
    answer = answer()
    if answer == 'all':
        df = psql.read_sql('select * from expenses',conn)
        df['month'] = df['trans_date'].apply(lambda x: x.month)
        df.groupby('month')['cost'].sum().plot.bar()
        plt.show()
    elif answer == 'separate':
        df = psql.read_sql("select date_part('month',trans_date),expense_type,sum(cost) from expenses group by expense_type,date_part('month',expenses.trans_date)",conn)
        sns.barplot(x=df['date_part'], y=df['sum'], hue=df['expense_type'])
        plt.show()
    else:
        print('There is no such an option')
        plot_month_bar()
