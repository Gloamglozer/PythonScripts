"""
LEGENDARY SIXTH PROBLEM
https://www.youtube.com/watch?v=Y30VF3cSIYQ
This is a quickly made script which visualizes a small grid containing solutions to the equation
given in the legendary sixth problem

something something vieta jumping
"""
from math import sqrt
import numpy

print("Legendary sixth problem\n")
space = 2
count = 0
numbers = False
grid = True
x = int(input("Enter the size you would like to see\n"))
if(grid):
    if(numbers):
        print(" ".rjust(space),end=" ")
        for k in range(0,x+1):
            print(str(k).rjust(space),end=" ")
        print(" ")
        for a in range(0,x+1):
            print(str(a).rjust(space),end=" ")
            for b in range(0,x+1):
                clark = (((a*a)+(b*b))/(a*b+1))
                if(sqrt(clark).is_integer()):
                    print(("!"+str(clark)).rjust(space),end=" ")
                    count +=1
                else:
                  print(str(round(clark,2)).rjust(space),end=" ")
            print(" ")
    else:
        print(" ".rjust(space),end=" ")
        for k in range(0,x+1):
            print(str(k).rjust(space),end=" ")
        print(" ")
        for a in range(0,x+1):
            print(str(a).rjust(space),end=" ")
            for b in range(0,x+1):
                clark = (((a*a)+(b*b))/(a*b+1))
                if(sqrt(clark).is_integer()):
                    print(("!").rjust(space),end=" ")
                    count +=1
                else:
                  print("x".rjust(space),end=" ")
            print(" ")
    print("\n")
    print(count-(2*x+1))
else:
    for a in range(0,x+1):
        for b in range(a,x+1):
            clark = (((a*a)+(b*b))/(a*b+1))
            if(sqrt(clark).is_integer()&(a!=0)):
                print(str("({},{})".format(a,b)).rjust(space))
                count +=1
            
              
