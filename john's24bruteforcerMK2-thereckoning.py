"""
24 BRUTE FORCER
quick whipped up for a friend to exhaustively find solutions to a question pertaining to the math game 24
"""

from itertools import product,permutations
class add:
    name = "+"
    def f(x,y):
        return x+y
class sub:
    name = "-"
    def f(x,y):
        return x-y
class mult:
    name = "*"
    def f(x,y):
        return x*y
class div:
    name = "/"
    def f(x,y):
        return x/y

operations = [add,sub,mult,div]
while(True):  
    numbers = [int(x) for x in input("enter 4 numbers seperated by spaces:\n").split()]
    count = 0
    for a,b,c,d in permutations(numbers):
        for first,second,third in product(operations,operations,operations):
            if(third.f(second.f(first.f(a,b),c),d) == 24 ):
                count += 1
                print("((({}{}{}){}{}){}{})".format(a,first.name,b,second.name,c,third.name,d)," = 24")
    
    print("There were {} ways to make 24".format(count))
