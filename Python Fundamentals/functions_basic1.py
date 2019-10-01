Assignment: Functions Basic I
Objectives:
Avoid common mistakes of using functions
Really understand how to use T-diagram to correctly predict and debug codes

________________________________________________________________________________
Predict the output
1) def a():
    return 5
print(a())
returns 5 

2) def a():
    return 5
print(a()+a())
returns 10 

3) def a():
    return 5
    return 10
print(a())
returns 5. It will not return 10 because after the first "return" line, the fx stops. 

4) def a():
    return 5
    print(10)
print(a())
returns 5 

5)def a():
    print(5)
x = a()
print(x)
prints 5 

6)def a(b,c):
    print(b+c)
print(a(1,2) + a(2,3))

prints 3 , 5 and none 

it returned an error that says "nonetype" not supported. 
 unsupported "operands" 
 This is because it stated "print" rather than "return". 

7) def a(b,c):
    return str(b)+str(c)
print(a(2,5))
this prints a string 25 

8) this prints 100 and returns 5

9) prints 7, 14 , 21 

10) prints 8 

11) prints 500,500,300,500

12) prints 500, 500, 300, 500

13) 500,500,500, 300, 300

14) 1,3,2 

15)  1,3,5,10 
