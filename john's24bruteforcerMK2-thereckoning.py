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

numbers = [int(x) for x in input("enter 4 numbers seperated by spaces:\n").split()]

for a,b,c,d in permutations(numbers):
    for first,second,third in product(operations,operations,operations):
        if(third.f(second.f(first.f(a,b),c),d) == 24 ):
            print("((({}{}{}){}{}){}{})".format(a,first.name,b,second.name,c,third.name,d)," = 24")
            
