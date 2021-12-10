# coding=utf-8

import re, datetime, os

# decimal seperator for string output
dec_sep = ','

# general ledger regex
PAT_TRANSACTION = re.compile(r'(\d{4,}.+(?:\n[^\S\n\r]{1,}.+)+)')
PAT_TRANSACTION_DATA = re.compile(r'(?P<year>\d{4})[/|-](?P<month>\d{2})[/|-](?P<day>\d{2})(?:=(?P<year_aux>\d{4})[/|-](?P<month_aux>\d{2})[/|-](?P<day_aux>\d{2}))? (?P<state>[\*|!])?[ ]?(\((?P<code>[^\)].+)\) )?(?P<payee>.+)')
PAT_COMMENT = re.compile(r'[^\S\n\r]{1,};(.+)')
PAT_ACCOUNT = re.compile(r'[^\S\n\r]{1,}(?P<account>[^;].+)(?:[^\S\n\r]{2,})(:?(?P<commodity_front>[^\d].+)?[^\S\n\r]{1,})?(?P<amount>[-+]?\d+[,|\.]?(?:\d+)?)?(?:[^\S\n\r]{1,}(?P<commodity_back>[^\d].+))?')
PAT_ACCOUNT_ONLY = re.compile(r'[^\S\n\r]{1,}(?P<account>[^;].+)')


# ledgerparse classes

class Money(object):
	def __init__(self, amount='0', real_amount=None, dec_sep=','):
		self.dec_sep = dec_sep
		self.amount = self.get_amount(amount) if real_amount == None else real_amount

	def get_amount(self, amount):
		# amount is zero, if amount is not a matching string
		if not type(amount) == str:
			amount = '0'

		# get rid of the thousand seperator
		if self.dec_sep == ',':
			amount = amount.replace('.', '')
		else:
			amount = amount.replace(',', '')

		# return integer from amount string

		# there is something behind the decimal seperator
		if self.dec_sep in amount:
			behind = amount.split(self.dec_sep)[1]
			if len(behind) == 1:
				behind += '000'
			elif len(behind) == 2:
				behind += '00'
			elif len(behind) == 3:
				behind += '0'
			elif len(behind) > 4:
				last_digit = int(behind[3])
				after_last_digit = int(behind[4])
				if after_last_digit >= 5:
					last_digit += 1
				behind = behind[:3] + str(last_digit)
			return int( amount.split(self.dec_sep)[0] + behind )

		# there is no decimal seperator at all
		else:
			return int( amount ) * 10000

	def str_amount(self):
		# amount is positive
		if self.amount > 0:
			# return something like 0,NNNN
			if self.amount < 10000:
				return '0' + self.dec_sep + self.behind_decimal( str(self.amount)[-4:] )
			# return something like N,NNN
			else:
				return str(self.amount)[:-4] + self.dec_sep + self.behind_decimal( str(self.amount)[-4:] )

		# amount is negative
		elif self.amount < 0:
			# return something like -0,NNNN
			if self.amount > -10000:
				return '-0' + self.dec_sep + self.behind_decimal( str(self.amount)[-4:] )
			# return something like -N,NNN
			else:
				return str(self.amount)[:-4] + self.dec_sep + self.behind_decimal( str(self.amount)[-4:] )

		# amount is zero
		else:
			return '0' + self.dec_sep + '00'

	def behind_decimal(self, value_string):
		# generate leading zeros
		if len(value_string) == 3:
			value_string = '0' + value_string
		elif len(value_string) == 2:
			value_string = '00' + value_string
		elif len(value_string) == 1:
			value_string = '000' + value_string

		# get rid of last zero at the end - two times
		if value_string[-1:] == '0':
			value_string = value_string[:-1]
		if value_string[-1:] == '0':
			value_string = value_string[:-1]

		return value_string

	def __lt__(self, other):
		return self.amount < other.amount

	def __le__(self, other):
		return self.amount <= other.amount

	def __gt__(self, other):
		return self.amount > other.amount

	def __ge__(self, other):
		return self.amount >= other.amount

	def __eq__(self, other):
		return self.amount == other.amount

	def __str__(self):
		return self.str_amount()

	def __int__(self):
		return self.amount

	def __repr__(self):
		return self.str_amount()

	def __add__(self, other):
		return Money(real_amount=self.amount+other.amount)

	def __sub__(self, other):
		return Money(real_amount=self.amount-other.amount)

	def __div__(self, other):
		return Money(real_amount=self.amount/other)

	def __mul__(self, other):
		return Money(real_amount=self.amount*other)


class ledger_transaction(object):
	def __init__(self, date, aux_date, state, code, payee, original):
		self.date = date
		self.aux_date = aux_date
		self.state = state
		self.code = code
		self.payee = payee
		self.comments = [] # [ str: comment ]
		self.accounts = [] # [ ledger_account ]
		self.original = original

	def __str__(self):
		# generat a transaction output string
		output = ''

		# get date
		tmp_date = self.date.strftime('%Y-%m-%d')

		# get aux date
		tmp_aux_date = '=' + self.aux_date.strftime('%Y-%m-%d') if self.aux_date != self.date else ''

		# get state
		tmp_state = ' ' + self.state if self.state else ''

		# get code
		tmp_code = ' (' + self.code + ')' if self.code else ''

		# get payee
		tmp_payee = ' ' + self.payee

		# get comments
		if len(self.comments) > 0:
			tmp_comments = '\n ;' + '\n ;'.join(self.comments)
		else:
			tmp_comments = ''

		# get accounts with its comments
		tmp_accounts = '\n' + '\n'.join( [str(x) for x in self.accounts] )

		# generate the output string
		output = tmp_date + tmp_aux_date + tmp_state + tmp_code + tmp_payee + tmp_comments + tmp_accounts

		return output

	def get_original(self):
		return self.original

	def add_account(self, name, commodity, amount):
		self.accounts.append( ledger_account(name, commodity, amount) )

	def add_comment_to_last_account(self, text):
		if len(self.accounts) > 0:
			self.accounts[ len(self.accounts)-1 ].add_comment(text)

	def add_comment(self, text):
		self.comments.append(text)

	def balance_account(self, id, negative=False):
		# get negatvie multiplicator
		multi = -1 if negative else 1

		# returns a Money object with the amount of the account with the given id
		own_amount = self.accounts[id].amount.amount
		if own_amount != 0:
			return Money(real_amount=self.accounts[id].amount.amount * multi)
		else:
			others = 0
			for which, acc in enumerate(self.accounts):
				if not which == id:
					others += acc.amount.amount
			return Money(real_amount=(own_amount - others) * multi )


class ledger_account(object):
	def __init__(self, name, commodity, amount):
		self.name = name
		self.commodity = commodity
		self.amount = Money(amount, dec_sep=dec_sep)
		self.comments = [] # [ str: comment ]

	def __str__(self):
		# generate an account output string
		output = ''

		# get the name
		tmp_name = self.name

		# get the commodity
		tmp_commodity = '  ' + self.commodity + ' ' if self.commodity else ''

		# get amount
		tmp_amount = str(self.amount) if self.amount.amount != 0 else ''

		# get comments
		tmp_comments = '\n ;' + '\n ;'.join(self.comments) if len(self.comments) > 0 else ''

		# return string for this account
		return ' ' + tmp_name + tmp_commodity + tmp_amount + tmp_comments

	def add_comment(self, text):
		self.comments.append(text)



# functions

def string_to_non_transactions(text):
	# returns a string with all the stuff in a ledger journal, which are no transactions

	# get original
	output = text

	# iterate every transaction
	for trans in PAT_TRANSACTION.findall(text):
		# delet this transaction from the output
		output = output.replace( trans, '' )

	# strip and return the output string
	return output.strip()


def string_to_ledger(text, aliases=False):
	# returns an array of [ledger_transaction]s from the given string (ledger-journal)

	# get aliases from file, if enabled
	if aliases:
		ALIAS = get_aliases_from_string(text)
	else:
		ALIAS = {}

	# init the output array
	output = []

	# iterate through all transaction-regex matches
	for trans in PAT_TRANSACTION.findall(text):
		output.append( string_to_transaction(trans, ALIAS) )

	# output the result
	return output


def string_to_transaction(text, aliases={}):
	# returns a [ledger_transaction] object from the given string

	# init variables
	last = 'None'

	# iterate through the lines of the string
	for line in text.splitlines():
		# do the matches
		m_trans			= PAT_TRANSACTION_DATA.match(line)
		m_comment		= PAT_COMMENT.match(line)
		m_account		= PAT_ACCOUNT.match(line)
		m_account_only	= PAT_ACCOUNT_ONLY.match(line)

		# the line is the transaction header
		if m_trans:

			# get the date
			tmp_date = datetime.datetime( int(m_trans.group('year')), int(m_trans.group('month')), int(m_trans.group('day')) )

			# get the aux date
			if m_trans.group('year_aux') != None and m_trans.group('month_aux') != None and m_trans.group('day_aux') != None:
				tmp_date_aux = datetime.datetime( int(m_trans.group('year_aux')), int(m_trans.group('month_aux')), int(m_trans.group('day_aux')) )
			else:
				tmp_date_aux = tmp_date

			# get the state
			if m_trans.group('state') != None:
				tmp_state = m_trans.group('state')
			else:
				tmp_state = ''

			# get the code
			if m_trans.group('code') != None:
				tmp_code = m_trans.group('code')
			else:
				tmp_code = ''

			# get the payee
			tmp_payee = m_trans.group('payee')

			# generate ledger_transaction output
			output = ledger_transaction(tmp_date, tmp_date_aux, tmp_state, tmp_code, tmp_payee, text)

			# set last to trans
			last = 'Trans'

		# the line is an account with commodity and an amount
		elif m_account and not last == 'None':

			# get its name
			tmp_name = m_account.group('account')
			# aliase it, if enabled / aliases exists
			if len(aliases) != 0:
				tmp_name = replace_alias(tmp_name, aliases)

			# get the commodity
			if m_account.group('commodity_front') != None:
				tmp_commodity = m_account.group('commodity_front')
			elif m_account.group('commodity_back') != None:
				tmp_commodity = m_account.group('commodity_back')
			else:
				tmp_commodity = ''

			# get the amount
			tmp_amount = m_account.group('amount')

			# add this account to the output ledger_transaction
			output.add_account(tmp_name, tmp_commodity, tmp_amount)

			# set last to Acc
			last = 'Acc'

		# the line is an account with only the account name
		elif m_account_only and not last == 'None':

			# get its name
			tmp_name = m_account_only.group('account')
			# aliase it, if enabled / aliases exists
			if len(aliases) != 0:
				tmp_name = replace_alias(tmp_name, aliases)

			# get the commodity
			tmp_commodity = ''

			# get the amount
			tmp_amount = '0'

			# add this account to the output ledger_transaction
			output.add_account(tmp_name, tmp_commodity, tmp_amount)

			# set last to Acc
			last = 'Acc'

		# the line is a comment
		elif m_comment and not last == 'None':

			# it belongs to the transaction
			if last == 'Trans':
				output.add_comment(m_comment.group(1))

			# it belongs to the last added account
			elif last == 'Acc':
				output.add_comment_to_last_account(m_comment.group(1))

	# output the ledger_transaction object
	return output if not last == 'None' else None


def ledger_file_to_string(ledger_file):
	# init the output variable
	OUT = ''

	# check if file exists and load it
	if os.path.isfile(ledger_file):
		f = open(ledger_file, 'r')
		FILE = f.readlines()
		f.close()
		# and get its path
		PATH = os.path.dirname( os.path.abspath(ledger_file) )
	else:
		return ''

	# append it to the final output, till "include" occurs
	for line in FILE:
		if line.lower().find('include ') != 0:
			OUT += line
		# otherwise try to load the given file
		else:
			# get filename
			include_me = line.replace('include ', '').replace('Include ', '').strip()

			# cycle through the files, if there are some and append their content
			# also replace wildcard with regex-wildcard
			regex = include_me.replace('.', '\.').replace('*', '.*')
			got_a_file = 0
			for filename in os.listdir(PATH):
				if re.match(regex, filename):
					if got_a_file != 0:
						OUT += '\n\n'
					got_a_file = 1
					f = open(os.path.join(PATH, filename), 'r')
					OUT += f.read()
					f.close()

			# newline at the end of the found "include ..." if there is one
			OUT += '\n' if '\n' in line else ''

	# return the final ledger journal string - bam!
	return OUT


def get_aliases_from_string(ledger_journal_string):
	# init output dict
	OUT = {}

	# cycle through ledger journal lines and find "alias" in the beginning of the line
	for l in ledger_journal_string.splitlines():
		if l[0:5] == 'alias':
			# get the alias
			tmp = l.replace('alias ', '').split('=')
			if len(tmp) == 2:
				OUT[tmp[0].strip()] = tmp[1].strip()

	# output the result
	return OUT


def replace_alias(original, replace_dict):
	# check if there are subaccounts and use the first
	if ':' in original:
		work_with_me = original[ 0:original.find(':') ]
		append = original[ original.find(':'): ]
	# or just use the original string
	else:
		work_with_me = original
		append = ''

	# check if the account is in the dict
	if work_with_me in replace_dict:
		return replace_dict[ work_with_me ] + append
	# or just return the original
	else:
		return original