import argparse

parser = argparse.ArgumentParser(description='Test for argparse')

parser.add_argument('-f', '--file', help='File to read', required=True)
parser.add_argument("command", default="print", choices=["balance", "register", "print"], help='Output file')

args = parser.parse_args()

try:
    with open(args.file) as f:
        data = f.readlines()[1:]
        f.close()
except FileNotFoundError:
    print('File not found')


if args.command == "print":
    for line in data:
        print(line)



if args.command == "balance":
    print("Balance Function")


if args.command == "register":
    print("Register Function")
