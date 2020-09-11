#!/usr/bin/python3
import itertools
import time
import os
# Used for the loading animation
import threading
import sys

doneLoading = False

def main():
	global doneLoading
	
	# For testing purposes
	# first_name = "First"
	# middle_name = "Middle"
	# last_name = "Last"
	# nickname = "Nick"
	# birth_year = "2022"
	# birth_month = "07"
	# birth_day = "04"
	# other = ""

	first_name = input("First name: ")
	nickname = input("Nickname: ")
	last_name = input("Last name: ")
	birth_year = input("Year of birth (YYYY): ")
	birth_month = input("Month of birth (MM): ")
	birth_day = input("Day of birth (DD): ")
	other = input("Other keywords (keyword1,keyword2,...): ")
	print("=================================")
	
	# Creates keywords
	names = [first_name, first_name.lower(), last_name, last_name.lower(), nickname, nickname.lower()]
	dates = [birth_year, birth_year[2:], birth_month, birth_day]
	if birth_month.startswith("0"):
		dates.append(birth_month[1:])
	if birth_day.startswith("0"):
		dates.append(birth_day[1:])
	numbers = ["123", "1234", "12345", "007", "321", "54321", "4321", "-", "_", "."]
	extended_numbers = ["12", "123456789", "1234567890", "987654321", "0987654321"]
	other_keywords = other.split(",")
	keywords = names + dates + numbers + other_keywords
	
	# Removes duplicate keywords
	keywords = list(set(keywords))
	# Removes blank keywords
	keywords = [string for string in keywords if string != ""]
	# Sorts the list
	keywords.sort()
	combs = []
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
	print("\nAmount of passwords: {}".format(len(combs)))
	print("Created in: " + str(end - start)[:5] + " seconds")
	print("Filesize: " + str(file_size("wordlist.txt")) + " MB")
	print("Filename name: wordlist.txt")


def makes_sense(password):
	if password.startswith(("-","_",".")) or password.endswith(("-","_",".")):
		return False
	elif any(s in password for s in (".-","._","-.","-_","_.","_-")):
		return False
	elif any(s in password for s in (".","_","-")) and password.startswith(("1","2","3","4","5","6","7","8","9","0")) and password.endswith(("1","2","3","4","5","6","7","8","9","0")):
		return False
	elif any(s in password for s in ("007",)) and password.startswith(("1","2","3","4","5","6","7","8","9","0")) and password.endswith(("1","2","3","4","5","6","7","8","9","0")):
		return False
	elif len(password)<=2:
		return False
	else:
		return True

def file_size(fname):
	'''Returns filesize in MB'''
	statinfo = os.stat(fname)
	return statinfo.st_size/1000000

def animate():
	for c in itertools.cycle(['.    ', '..   ', '...  ', '.... ', '.....']):
		if doneLoading:
			break
		sys.stdout.write('\rCreating passwords (this may take a while) ' + c)
		sys.stdout.flush()
		time.sleep(0.1)
    # sys.stdout.write('\rDone!\n')

if __name__ ==  "__main__":
	main()