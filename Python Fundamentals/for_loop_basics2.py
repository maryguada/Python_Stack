Assignment: For Loop Basic II
Objectives:
Get comfortable writing functions only using basic building blocks of Python (i.e. using your own skills rather than relying on built-ins)
Get comfortable using for loops, functions, lists, and other data types
_____________________________________________________________________________________________________________________

###1 Biggie Size 
def BiggieSize(arr): 
""" Changes all the positive numbers in list to string 'big' """
    for i in range(len(arr)): 
        if arr[i] >0:
            arr[i]= "big"
    return arr

print(BiggieSize([-1,-2,3,4]))


###2 Count Positives 
def count_positives(arr):
""" Replaces the last value with the number of positive values inside the list """
    counter = 0  
    for i in range(len(arr)): 

        if arr[i] > 0 : 

            counter +=1 

    arr[len(arr)-1] = counter  
    return arr

print (count_positives([2,3,-1,-3]))


###3 Sum Total 
def sumtotal(arr): 
""" Returns the sum of all the values in the array. """
    total = 0 
    for item in arr: 
        total += item 
    return total 
print(sumtotal([1,3,4]))


###4 Average
def average(arr): 
"""  Takes a list and returns the average of all the values. """
    total = 0 
    for item in arr: 
        total += item 
    return total / len(arr)

print(average([0,1,2,3,4]))

####5 Length 
def length(arr): 
""" Takes a list and returns the length of the list. """
    return len(arr)

print(length([2,3,4,5,6]))

###6 Minimum 
def minimum(arr): 
""" Takes a list of numbers and returns the minimum value in the list. """
    min = arr[0]
    for i in range(1,len(arr)): 
        if arr[i]<arr[0]:
            min = arr[i]

    return min 
print(minimum([2,3,5,6]))


###7 Maximum 
def maximum(arr):
""" Takes a list and returns the maximum value in the array. """
    max = arr[0]
    for i in range(1, len(arr)): 
        if arr[i] > arr[0]: 
            max = arr[i]

    return max

print(maximum([2,3,4,5,6]))


###8 Ultimate Analysis 
def ultimate_analize(arr):
""" Takes a list and returns a dictionary that has the sumTotal, average, minimum, maximum and length of the list."""
    dict = {
        'sumtotal' : sum_total(arr),
        'avg' : average(arr),
        'min' : minimum(arr),
        'max' : maximum(arr),
        'len' : length(arr)
    }
    return dict


###9 Reverse List 
def reverse_list(arr): 
"""Takes a list and return that list with values reversed, without creating a second list."""
    for i in range(0, len(arr)/2): 
        temp = arr[i]
        arr[i] = arr[len(arr)-i-1]
        arr[len(arr)-i-1] = temp
    return arr

print (reverse_list([0,1,2,3,4,5,6,7,8]))

