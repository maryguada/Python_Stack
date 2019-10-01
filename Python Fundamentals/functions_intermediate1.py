Assignment: Functions Intermediate I
Objectives:
Practice using default parameter values
Practice passing in named arguments
Become familiar with Python's random module
_______________________________________________

With this concept of default parameters in mind, the goal of
this assignment is to write a single function, randInt() that 
takes up to 2 arguments.

import random 
def randInt(min=0, max=100):
    if min>max:
        return 'Invalid numbers'
    if max < 0:
        return 'Invalid numbers'
    return round(random.random() *  max) + min

print(randInt(-8, 3))
