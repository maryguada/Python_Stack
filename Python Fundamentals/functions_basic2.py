Assignment: Functions Basic II
Objectives:
Learn how to create basic functions in Python
Get comfortable using lists
Get comfortable having the function return an expression/value

________________________________________________________________
### 1. Countdown.
def Countdown(number): 
""" Returns a new list that counts down by one, from the number given as a parameter."""
  for x in range(number, 0, -1):
    print (x)
    
print(Countdown(5))

### 2. Print and Return.
def Print_Return(nums): 
"""  Takes in an array with two numbers. Print the first value and return the second. """
    print(nums[0])
    return(nums[1])

Print_Return([2,5])


### 3. First plus length.
def first_plus_length(arr): 
""" Accepts a list and returns the sum of the first value in the lists plus its length"""
    return arr[0] + len(arr)

first_plus_length([1,2,3,4,5])


### 4. Values greater than second.
def greater_than_second(arr): 
""" Returns a new list containing values that are greater than the 2nd val in the orig list. 
& prints how many values there is"""
    new_list = []
    counter = 0

    for i in range(len(arr)): 
        if arr[i] > arr[1]: 
            new_list.append(arr[i])
            counter +=1 
     
    print(new_list)
    print(counter)
        
greater_than_second([1,2,3,4,5])

###5 This length that value. 
def length_value(i,j):
""" Write a function that accepts two integers as parameters: size and value. 
The function should create and return a list whose length is equal to the given size,
and whose values are all the given value. """

    var = []

    for item in range(0,i): 
        if var.append(j)
        return var 
        
