# for basic learning of bloom filters: https://llimllib.github.io/bloomfilter-tutorial/
# for concatenating integers with characters: https://stackoverflow.com/questions/11559062/concatenating-string-and-integer-in-python
# for getting random ascii characters: https://stackoverflow.com/questions/2823316/generate-a-random-letter-in-python
# for getting random integers: https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/
# for concatenating items in a list: https://stackoverflow.com/questions/12453580/concatenate-item-in-list-to-strings
# for use of hashing algorithm: Lab 5 from class
# for probability of false positives and more on bloom filters: https://en.wikipedia.org/wiki/Bloom_filter
# for use of power function and e constant: https://docs.python.org/2/library/math.html
# for some float to integer issues I was having: https://stackoverflow.com/questions/4730949/how-do-i-do-simple-user-input-in-python
# https://stackoverflow.com/questions/19824721/i-keep-getting-this-error-for-my-simple-python-program-typeerror-float-obje

import math
import hashlib
import random
import string
import time

print("\nWelcome to the bloom filter for detecting email spam!\n")

print("\nWe will be using 1 hash function, so our k value is 1.")
k = 1

while (1):	# error detection on user input
	try:
		n = int(input("Choose a value for n where n is the number of elements we want to filter: "))
		if (n >= 0):
			break
		else: n = int(input("Try again: "))
		if (n >= 0):
			break
	except ValueError:
		print("Not a valid entry for n")
while (1):
	try:
		sp = float(input("Choose a percentage of the elements to be spam (e.g. for 10% to be spam you would input 0.1): "))
		if (sp <= 1 and sp >= 0):
			break
		else: sp = float(input("Must choose a value between 0 and 1: "))
		if (sp <= 1 and sp >= 0):
			break
	except ValueError:
		print("Not a valid entry")
while (1):
	try:
		m = int(input("Choose a value for m where m is the number of bits used in the bloom filter (increase this value for improved spam detection!): "))
		if (m >= 0):
			break
		else: m = int(input("Try again: "))
		if (m >= 0):
			break
	except ValueError:
		print("Not a valid entry for m")

accepted = [] #list of accepted emails
spam = [] #list of spam
incoming = [] # list of incoming emails (combination of spam/accepted)
domain = ["@gmail.com", "@hotmail.com", "@yahoo.com", "@aol.com", "@shaw.ca", "@telus.net", "@outlook.com", "@msn.com", "@icloud.com", "gmail.ca"]
bitArray = [0]*int(m) # increasing array size improves spam detection while decreasing size will reduce it 
bitArray2 = [0]*int(m)

for i in range(int(n)): # create list of n random accepted emails
	id = []
	newId = ""

	for x in range(3):
		letter = random.choice(string.ascii_lowercase)
		id += letter
	for y in range(2):
		id.append(str(random.randint(0,9)))

	random.shuffle(id)
	newId = ''.join(id)
	newDomain = random.choice(domain)
	email = newId + newDomain
	accepted.append(email)

for i in range(int(n)): # create list of n random spam emails
	id = []
	newId = ""

	for x in range(3):
		letter = random.choice(string.ascii_lowercase)
		id += letter
	for y in range(2):
		id.append(str(random.randint(0,9)))

	random.shuffle(id)
	newId = ''.join(id)
	newDomain = random.choice(domain)
	email = newId + newDomain
	spam.append(email)

# now we create a list of incoming emails (mix of random accepted and random spam)
y = sp*n
for i in range(int(n - y)):
	choose_accepted = random.choice(accepted)
	incoming.append(choose_accepted)
for i in range(int(y)):	
	choose_spam = random.choice(spam)
	incoming.append(choose_spam)

random.shuffle(incoming)

print("\nList of incoming emails: \n\n",incoming)

# first we hash the list of accepted emails
for i in range(int(n)):
	new_hash_object = hashlib.md5(accepted[i].encode('utf-8'))
	new_hash_hex = new_hash_object.hexdigest()
	new_hash_int = int(new_hash_hex, 16)
	new_hash_abs = abs(new_hash_int)
	new_hash_index = new_hash_abs % len(bitArray)
	bitArray[new_hash_index] = 1


print("\nBit array representing accepted emails:\n" , bitArray)

bitArray2 = bitArray # making a copy of the array
x = 0
accepted_incoming = incoming

# now we hash the list of incoming emails
for i in range(int(n)):
	new_hash_object = hashlib.md5(incoming[i].encode('utf-8'))
	new_hash_hex = new_hash_object.hexdigest()
	new_hash_int = int(new_hash_hex, 16)
	new_hash_abs = abs(new_hash_int)
	new_hash_index = new_hash_abs % len(bitArray2)
	if (bitArray[new_hash_index] == 0): # compare the indexes
		bitArray2[new_hash_index] = 1 # if 0 becomes 1 -> spam
		time.sleep(1)
		print("\nIncoming email", incoming[i], "is spam")
		x = x + 1
	else: 
		bitArray2[new_hash_index] = 1 
print("\n\t",((x/y)*100), "\b% of all spam was detected.")
time.sleep(1) # sleep to simulate live feed 
print("\nSame bit array after hashing incoming emails:\n", bitArray2)
falsePositive = math.pow(1 - (math.pow(math.e, (-k*n)/m)), k) # false positive formula
print("\n\tProbability of a false positive = ", falsePositive, "\n")
