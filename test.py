import argparse


parser = argparse.ArgumentParser(
    prog='ledgertruji',
    description='A simple Ledger CLI application in Python',
    epilog='Created by: Adrian Trujillo in the Apprentice Program by Encora.')

parser.add_argument('-f', '--file', help='Input a file to read.', required=True)
parser.add_argument('-s', '--sort', help='Sort by date.')
parser.add_argument('--price-db', nargs=2, help='Load a DB for currencies and commodities.')
parser.add_argument("command",
    choices=['balance', 'bal','register', 'reg', 'print'],
    help='Select a command to implement.')
parser.add_argument('--filter', nargs='*', help='Filter by account.')

#Parsing the inputed arguments
args = parser.parse_args()

#Calling the functions defined above, depending on the inputed commands and flags

#File flag
if args.file:
    print('File:', args.file)

#Sort flag
if args.sort:
    print('Sort:', args.sort)

#Price DB flag
if args.price_db:
    print('Price DB:', args.price_db)

#Commands
if args.command == 'print':
    print('Printing...')

if args.command in ['balance', 'bal']:
    print('Balance...')

if args.command in ['register', 'reg']:
    print('Register...')

if args.filter:
    print('Filtering...' + args.filter[0] + args.filter[1])