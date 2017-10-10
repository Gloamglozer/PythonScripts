import random

trials = 10000000
x=1000
summ = 0
for i in range(trials):
    r = random.uniform(0,x)
    n = 1
    while(r>=1):
        r = random.uniform(0,r)
        n += 1
    summ+=n
    if(i%1000000==0):
        print("-------")
print(summ/trials)
    

    
