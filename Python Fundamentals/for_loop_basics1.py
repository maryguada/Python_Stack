Assignment: For Loops: Basic I
Objectives:
Learn how to use basic for loop statements in Python
Practice some basic algorithms in Python
___________________________________________________

#1 Basic - Print all integers from 0 to 150 
for i in range(151):
    print(i)

#2 Multiple of Five. Print all the multiples of 5 from 5 to 1000
for i in range(5, 5001): 
    if i % 5 == 0: 
        print (i)
        
#3 Counting the Dojo Way. Print integers 1 to 100. if divisible by 5 print ="coding". if divisible by 
# ten print "dojo".
for i in range(1, 101):
    if (i % 10 == 0): 
        print("Coding Dojo")
    elif (i % 5 == 0):
        print("Coding")
    else: 
        print(i)

#4 Add odd integers from 0 - 500,000 and print the final sum 
total = 0 
for i in range(1, 500001, 2): 
    total +=i        
print(total)

#5 Countdown by fours 
total = 2018 
while (total >= 0):
    print (total)

    total = total - 4 

    if total == 0: 
        break

#6  Flexible Counter 
low = 2 
high = 9 
mult = 3 

for i in range(low, high, mult): 
    if (i%mult == 0): 
        print(i)

