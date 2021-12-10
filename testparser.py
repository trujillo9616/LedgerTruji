
import re
try:
    with open("Receivable.ledger") as f:
        data = f.readlines()[1:]
        f.close()
except FileNotFoundError:
    print('File not found')

transactions = []

class Transaction:
    def __init__(self, date, comment, account1, amount1, account2):
        self.date = date
        self.comment = comment
        self.account1 = account1
        self.amount1 = [amount1[0], float(amount1[1:])]
        self.account2 = account2
        self.amount2 = [amount1[0], float(amount1[1:]) *- 1]


def print_date(data):
    for line in data:
        line = line.replace('/', '-')
        match = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})', line, re.M|re.I)
        if match:
            firstline = line.split(" ", 1)
            print('Date: ', firstline[0])
            print('Comment: ', firstline[1])
        else:
            print('Not a date')

print_date(data)

def print_transaction_info(data):
    for line in data:
        line = line.replace('/', '-')
        match = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})', line, re.M|re.I)
        if not match:
            items = line.split('\t')
            for item in items:
                items.remove(item)
            print()


# def format_amount(amount):
#     "Format unit/currency as a string."

#     if amount == {}:
#         return "-"

#     units = amount['units']
#     quantity = amount['quantity']

#     if quantity >= 0:
#         return "${0:,.2f}".format(quantity/100.00)
#     else:
#         return "-${0:,.2f}".format(quantity/100.00)