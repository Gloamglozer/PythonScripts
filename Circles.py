"""
POLYGON OPTIMIZING GENERATIONAL ALGORITHM 
this program attempts to optimize randomly seeded polygons to be circular using a naive generational algorithm
M starts the algorithm
N stops the algorithm
"""
import sys
import pygame
from random import randint
import itertools
from collections import OrderedDict
import pickle as p

#counting the number of times executed for unique data dumps after each execution (not implemented)
f = open("execution_index.pkl",'rb')
execution_index = p.load(f)
execution_index +=1
f.close
# execution_index = 0
f = open("execution_index.pkl",'wb')
p.dump( execution_index, f)
f.close()
print(execution_index)

class Polygon:
    def __init__(self, n,max_x, max_y):
        self.n = n
        self.max_x = max_x
        self.max_y = max_y
        self.pointlist = []
        for i in range(n):
            self.pointlist.append((randint(0,max_x),randint(0,max_y))) 
        self.findFitness()

    def plot(self, offset):
        offsetPoints = [(x[0]+offset[0],x[1]+offset[1]) for x in self.pointlist]
        pygame.draw.polygon(screen,
                            (0xff,0xff,0xff),\
                            # True, \
                            offsetPoints)

    def findFitness(self):
        # finding the area of the polygon http://www.mathopenref.com/coordpolygonarea.html
        # due to this algorithm for calculating the area, counter clockwise and clockwise areas cancel out
        # so there is extra punishment for being self-intersecting
        area  = 0 
        for i in range(self.n):
            point = self.pointlist[i]
            nextPoint = self.pointlist[(i+1)%self.n]
            area += (point[0]*nextPoint[1])-(nextPoint[0]*point[1])
        area = abs(area)/2
        #finding the perimeter of the polygon 
        perimeter = 0
        for i in range(self.n):
            point = self.pointlist[i]
            nextPoint = self.pointlist[(i+1)%self.n]
            perimeter += ((nextPoint[0]-point[0])**2+(nextPoint[1]-point[1])**2)**.5
        #squaring it so the fitness function is only circle-ness and does not incentivize size
        self.fitness = area/(perimeter**2) 
        return self.fitness


    def mutate(self, mutationRate): # returns a mutated version of self, does not edit self 
        mutatedPoints = []
        for i in range(self.n):
            potentialPoint = -1 # setting a value that will enter the while loop
            while(potentialPoint<0 or potentialPoint>=self.max_x): #making sure the point is valid
                #adding a random number to all of the coordinates in the polygon
                potentialPoint = randint(-mutationRate,mutationRate)+self.pointlist[i][0] 
            mutatedX = potentialPoint
            potentialPoint = -1
            while(potentialPoint<0 or potentialPoint>=self.max_y):
                potentialPoint = randint(-mutationRate,mutationRate)+self.pointlist[i][1]
            mutatedY = potentialPoint
            mutatedPoints.append((mutatedX,mutatedY)) 
        return mutatedPoints

class Generation:
    def __init__(self, x, y, size,pointsPerPolygon):
        self.x = x
        self.y = y
        self.cellx = int(size[0]/x)
        self.celly = int(size[1]/y)
        self.size = size
        self.numPolygons = x*y
        self.offsets =[]
        self.polys = []
        self.bestPolys = []
        for i,j in itertools.product(range(self.x),range(self.y)):
            self.offsets.append((i*self.cellx,j*self.celly))
        for i in range(self.numPolygons):
            self.polys.append(Polygon(pointsPerPolygon,self.cellx,self.celly))


    def plot(self):
        # drawing dividers
        for i in range(1,self.x):
            pygame.draw.line(screen,(0x80,0x80,0x80),(i*self.cellx,0),(i*self.cellx,size[1]))
        for i in range(1,self.y):
            pygame.draw.line(screen,(0x80,0x80,0x80),(0,i*self.celly),(size[0],i*self.celly))
        for i in range(self.numPolygons):
            self.polys[i].plot(self.offsets[i])

            ren = font.render('{0:.7f}'.format(self.polys[i].fitness), 0,(200,0,0) )
            screen.blit(ren, self.offsets[i])

        
    def newGen(self, mutationRate):
        # this is the function that performs the logic for making a new generation
        fitnessDict = OrderedDict()
        for poly in self.polys:
            fitnessDict[poly.fitness] = poly # each object is added to an ordered dict indexed by their fitness
        fitnessDict = OrderedDict(sorted(fitnessDict.items()))
        fitnessDict = OrderedDict(reversed(fitnessDict.items())) # sort the items from lowest to highest  fitness
        for poly in self.polys:
            # for now, there is no crossover and we're only mutating using the best offspring as a starting point
            poly.pointlist =  list(fitnessDict.items())[0][1].mutate(mutationRate) # call mutate on the object with the highest fitness
            poly.findFitness() # with the new generation of points, find their fitnesses for plotting. 
        



pygame.init()
pygame.font.init()

size = width, height = 1200, 600
#start with a random seed, x and y are the number of rows and columns which the individuals are displayed in
gen = Generation(8,4,size,pointsPerPolygon = 20)
screen = pygame.display.set_mode(size)

font = pygame.font.Font(None, 30)
makeNewGen = False 
while 1:
   
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m: #M plays the algorithm
                makeNewGen = True
            if event.key == pygame.K_n: #N stops the algorithm
                makeNewGen = False

    if makeNewGen:
        gen.newGen(mutationRate=1)

    gen.plot()
    
    pygame.display.flip()