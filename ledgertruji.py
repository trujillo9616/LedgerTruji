#This is a fun short project of a Ledger CLI implementation in Python

#Imports
from os import read
import re
import argparse
import datetime
import collections
import numpy as np
from tabulate import tabulate
from colored import fg


#Defining helper variables
data = []
data_prices = []
transactions = []
sort = False
balance = collections.defaultdict(float)
exchange = collections.defaultdict(float)
purple = fg('blue')
white = fg('white')
red = fg('red')
defaultcurrency = '$'

#Defining the Transaction class
class Transaction:
    def __init__(self, date, comment, account1, amount1, account2, amount2=None):
        self.date = date
        self.comment = comment
        self.account1 = account1
        self.account2 = account2

        #If there is not amount 2 defined
        if not amount2:
            #COMODITY
            if (' ' in amount1):
                amount = amount1.split(' ')
                self.amount1 = [amount[1], float(amount[0])]
                self.amount2 = [amount[1], float(amount[0]) * -1]
            #AMOUNT
            else:
                if ('-' in amount1):
                    amount1 = amount1.replace('-', '')
                    self.amount1 = [amount1[0], float(amount1[1:])* -1]
                    self.amount2 = [amount1[0], float(amount1[1:])]
                else:
                    self.amount1 = [amount1[0], float(amount1[1:])]
                    self.amount2 = [amount1[0], float(amount1[1:])* -1]

        #THERE IS AMOUNT 1 AND AMOUNT 2
        else:
            #Am1 Comodity
            if (' ' in amount1):
                amount = amount1.split(' ')
                self.amount1 = [amount[1], float(amount[0])]
            #Am1 Amount
            else:
                if ('-' in amount1):
                    amount1 = amount1.replace('-', '')
                    self.amount1 = [amount1[0], float(amount1[1:])* -1]
                else:
                    self.amount1 = [amount1[0], float(amount1[1:])]

            #A2 Comodity
            if (' ' in amount2):
                amount = amount2.split(' ')
                self.amount2 = [amount[1], float(amount[0])]
            #Am2 Amount
            else:
                if ('-' in amount2):
                    amount2 = amount2.replace('-', '')
                    self.amount2 = [amount2[0], float(amount2[1:])* -1]
                else:
                    self.amount2 = [amount2[0], float(amount2[1:])]


#READFILE Function
def readfile(filename):
    """
    readfile Function: Reads an input file provided by the user.

    :param filename: Define the file's location.

    :return: Nothing. Creates a data variable with the file's content.
    """
    try:
        with open(filename) as f:
            for line in f.readlines():
                if line.startswith(';'):
                    continue
                if line.startswith('!include'):
                    readfile(line.split()[1])
                    continue
                data.append(line)
    except FileNotFoundError:
        print('File not found, please check the file name')
        exit()


#READ PRICE-DB Function
def read_pricedb(filename):
    """
    read_pricedb Function: Parses a Price-DB file and stores the content variable exchange.

    :param filename: Define the file's location.

    :return: Nothing. Creates an exchange variable with the file's content
    """
    exchange['$'] = 1.0
    pattern = re.compile(r'\b\d[\d,.]*\b')
    try:
        with open(filename) as f:
            for line in f.readlines():
                if line.startswith('N'):
                    continue

                if line.startswith('D'):
                    defaultcurrency = re.sub(pattern, '', line.split(' ', 1)[1]).strip()

                if line.startswith('P'):
                    symbol, exrate = line.split(' ', 3)[3].split(' ')
                    exchange[symbol] = float(re.findall(pattern, exrate)[0])
    except FileNotFoundError:
        print('Price-DB file not found, please check the file name')
        exit()


#EXCHANGE Function
def exchange_values(transactions, exchange, currency=defaultcurrency):
    """
    exchange_values Function: Exchange the currencies or commodities to the specified one, using
    the data from price-db.

    :param transactions: The transactions array with the data.
    :param exchange: A dictionary with the exchange rates.
    :param currency: The destination currency.

    :return: Nothing. Modifies the amounts and currencies in the transactions array.
    """
    for tr in transactions:
        if not tr.amount1[0] == currency:
            if not tr.amount1[0] == '$':
                tr.amount1[1] *= exchange[tr.amount1[0]]
                tr.amount1[0] = '$'

            tr.amount1[1] /= exchange[currency]
            tr.amount1[0] = currency

        if not tr.amount2[0] == currency:
            if not tr.amount2[0] == '$':
                tr.amount2[1] *= exchange[tr.amount2[0]]
                tr.amount2[0] = '$'

            tr.amount2[1] /= exchange[currency]
            tr.amount2[0] = currency


#PARSE Function
def parse(data):
    """
    parse Function: Parses the information stored in the data variable.

    :param data: Data variable containing the information to be parsed.

    :return: Nothing. Creates a transactions array with Transaction objects of the
    parsed information.
    """
    for i in range(0, len(data), 3):
        #First line (DATE & COMMENT)
        data[i] = data[i].replace('/', '-').strip('\n')
        firstline = data[i].split(' ', 1)
        date = np.array(firstline[0].split('-')).astype(int)
        date = datetime.date(date[0], date[1], date[2])
        comment = firstline[1]

        #Second line (ACCOUNT1 & AMOUNT1)
        secondline = data[i+1].strip('\n').split('\t')
        for item in secondline:
            if item == '':
                secondline.remove(item)
        account1 = secondline[0].strip()
        amount1 = secondline[1]

        #Third line (ACCOUNT2 & AMOUNT2)
        thirdline = data[i+2].strip('\n').split('\t')
        for item in thirdline:
            if item == '':
                thirdline.remove(item)
        account2 = thirdline[0].strip()
        if len(thirdline)>1:
            amount2 = thirdline[1]
        else:
            amount2 = None

        transactions.append(Transaction(date, comment, account1,
        amount1, account2, amount2))


#PRINT COMMAND
def print_ledger(transactions, sort=False, *regex):
    """
    print_ledger Function: Print the ledger transactions of the inputed file.

    :param transactions: transactions array containing the parsed information.
    :param sort: Boolean variable to sort the transactions by date.
    :param regex: Array of regular expressions to filter the transactions.

    :return: Print onto console the transactions of the ledger.
    """

    #Sort the transactions
    if sort:
        transactions.sort(key=lambda x: x.date)

    #Print the transactions
    for t in transactions:
        print(str(t.date) + ' ' + '{:<30}'.format(t.comment))
        print('\t\t' + (purple+'{:30}'.format(t.account1)+white) + '\t\t\t\t' + t.amount1[0]+''+str(t.amount1[1]))
        if abs(t.amount1[1]) == abs(t.amount2[1]):
            print('\t\t' + (purple+'{:30}'.format(t.account2)+white))
        else:
            print('\t\t' + (purple+'{:30}'.format(t.account2)+white) + '\t\t\t\t' + t.amount2[0]+''+str(t.amount2[1]))



#REGISTER COMMAND
def register_ledger(transactions, sort=False, *regex):
    """
    register_ledger Function: Prints a register of the transactions.

    :param transactions: transactions array containing the parsed information.
    :param sort: Boolean variable to sort the transactions by date.
    :param regex: Array of regular expressions to filter the transactions.

    :return: Print onto console the register of the transactions.
    """
    headers = ['Date', 'Comment', 'Account', 'Amount', 'Balance']
    register = []
    balance = collections.defaultdict(float)

    #Sort the transactions
    if sort:
        transactions.sort(key=lambda x: x.date)

    #Make the register
    for t in transactions:
        #Update the balance for amount 1
        balance[t.amount1[0]] += t.amount1[1]
        register.append([t.date, t.comment, purple+t.account1+white, t.amount1[0] + ' ' +
        str(t.amount1[1]), ''.join('%s %.2f\n'% (key, val) for (key, val) in balance.items())])
        #Update the balance for amount 2
        balance[t.amount2[0]] += t.amount2[1]
        register.append(['', '', purple+t.account2+white, t.amount2[0] + ' ' + str(t.amount2[1]),
        ''.join('%s %.2f\n'% (key, val) for (key, val) in balance.items())])
        register.append(['- ',' ',' ',' ',' '])

    print(tabulate(register, headers))



#BALANCE COMMAND
def balance_ledger(transactions, *regex):
    """
    balance_ledger Function: Prints a balance of the accounts.

    :param transactions: transactions array containing the parsed information.
    :param regex: Array of regular expressions to filter the transactions.

    :return: Print onto console the balance of the accounts.
    """
    pass








#CLI Application Implementation
parser = argparse.ArgumentParser(
    prog='ledgertruji',
    description='A simple Ledger CLI application in Python',
    epilog='Created by: Adrian Trujillo in the Apprentice Program by Encora.')

parser.add_argument('-f', '--file', help='Input a file to read.', required=True)
parser.add_argument('-s', '--sort', help='Sort by date.')
parser.add_argument('--price-db', help='Load a DB for currencies and commodities.')
parser.add_argument("command",
    default="print",
    choices=['balance', 'bal','register', 'reg', 'print'],
    help='Select a command to implement.')

#Parsing the inputed arguments
args = parser.parse_args()


#Calling the functions defined above, depending on the inputed commands and flags

#File flag
if args.file:
    readfile(args.file)
    parse(data)

if args.sort:
    sort = True

if args.price_db:
    read_pricedb(args.price_db)
    print(exchange)


#Commands
if args.command == 'print':
    print_ledger(transactions, sort)

if args.command in ['balance', 'bal']:
    print("Balance Function")

if args.command in ['register', 'reg']:
    register_ledger(transactions, sort)