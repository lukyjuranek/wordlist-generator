#!/usr/bin/python3
import itertools
import time
import os
import re
# Used for the loading animation
import threading
import sys

doneLoading = False

class colors:
    purple = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    warning = '\033[93m'
    red = '\033[91m'
    end = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
	global doneLoading
	# For testing purposes
	first_name = "First"
	middle_name = "Middle"
	last_name = "Last"
	nickname = "Nick"
	birth_year = "2022"
	birth_month = "07"
	birth_day = "04"
	other = ""

	# first_name = input("First name: ")
	# nickname = input("Nickname: ")
	# last_name = input("Last name: ")
	# birth_year = input("Year of birth (YYYY): ")
	# birth_month = input("Month of birth (MM): ")
	# birth_day = input("Day of birth (DD): ")
	# other = input("Other keywords (keyword1,keyword2,...): ")
	print("=================================")
	
	# Creates keywords
	names = [first_name, first_name.lower(), reverse(first_name), last_name, last_name.lower(), reverse(last_name), nickname, nickname.lower(), reverse(nickname)]
	dates = [birth_year, birth_year[2:], birth_month, birth_day]
	if birth_month.startswith("0"):
		dates.append(birth_month[1:])
	if birth_day.startswith("0"):
		dates.append(birth_day[1:])
	numbers = ["123", "1234", "12345", "007", "321", "54321", "4321", "-", "_", ".", "#"]
	extended_numbers = ["12", "123456789", "1234567890", "987654321", "0987654321"]
	other_keywords = other.split(",")
	keywords = names + dates + numbers + other_keywords
	common_words = ['qwerty', 'qwertz', 'asdfg', 'asdfgh']
	
	# Removes duplicate keywords
	keywords = list(set(keywords))
	# Removes blank keywords
	keywords = [string for string in keywords if string != ""]
	# Sorts the list
	keywords.sort()
	# The final list that's is written into a file
	combs = []
	combs.append(common_words)
	# TODO: function that creates keywords

	start = time.time()
	# Starts the loading animation
	t = threading.Thread(target=animate)
	t.start()
	# Creates combinations
	for i in range(1,6):
		for combination in list(itertools.permutations(keywords, i)):
			joined = ''.join(combination)
			# Remove nonsense passwords
			if makes_sense(joined):
				combs.append(joined)
			else:
				continue

	# Write the wordlist into a file
	with open('wordlist.txt', 'w') as f:
		for item in combs:
			f.write("%s\n" % item)

	# Measures the execution time
	end = time.time()
	# Stops the loading animation
	doneLoading = True
	# Print info
	print("\nAmount of passwords: {}{}{}".format(colors.blue, f'{len(combs):,}', colors.end))
	print("Created in: " + colors.blue + str(end - start)[:5] + " seconds" + colors.end)
	print("Filesize: " + colors.blue + str(file_size("wordlist.txt")) + " MB" + colors.end)
	print("Filename name: {}{}wordlist.txt{}".format(colors.UNDERLINE, colors.green, colors.end))


def makes_sense(password):
	'''Returns True if the password makes sense'''

	letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', 'A', 'B', 'C', 'D', 'E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
	numbers = ("1","2","3","4","5","6","7","8","9","0")

	if len(password)<=2:
		# Smaller than 2 characters
		return False
	elif password.startswith(("-","_",".","#")) or password.endswith(("-","_",".")):
		return False
	elif any(s in password for s in (".-","._","-.","-_","_.","_-")):
		# abcd.-123
		return False
	elif any(s in password for s in (".","_","-")) and password.startswith(numbers) and password.endswith(numbers):
		# 123-123
		return False
	elif any(s in password for s in letters) and password.startswith(numbers) and password.endswith(numbers):
		# 123abc123
		return False
	elif any(s in password for s in ("007",)) and password.startswith(numbers) and password.endswith(numbers):
		# 123abc007
		return False
	elif re.search("\d+[a-zA-Z]+\d+", password):
		# 123abc123
		return False
	elif re.search("\d+\D\D+\d+", password):
		# digits with at least two non-digits between them
		# 123.a123
		return False
	else:
		return True

def file_size(fname):
	'''Returns filesize in MB'''
	statinfo = os.stat(fname)
	return statinfo.st_size/1000000

def animate():
	'''Makes the loading animation'''
	for c in itertools.cycle(['.    ', '..   ', '...  ', '.... ', '.....']):
		if doneLoading:
			break
		sys.stdout.write('\rCreating passwords (this may take a while) ' + c)
		sys.stdout.flush()
		time.sleep(0.2)
    # sys.stdout.write('\rDone!\n')

def reverse(value):
	return str(value)[::-1]

if __name__ ==  "__main__":
	main()