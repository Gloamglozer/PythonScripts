import math
def ncr(n,k):
    return (math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))

def binprob(n, p, a, b):
    s = 0
    if(isinstance(n,int)and(isinstance(a,int))and(isinstance(b, int))and(0<p)and(p<1)):
        for i in range(a, b+1):
            s += ncr(n,i)*(p**i)*((1-p)**(n-i))
        return s
    else:
        print("Nonvalid inputs")
        return None
    
print(binprob(10,.2,2,10)/(binprob(10,.2,1,10)))
