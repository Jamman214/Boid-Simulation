import random
import math
from numba import njit
import pygame
import numpy as np
import time

def genVec():
    angle = random.random() * 2 * math.pi
    vector = [math.cos(angle), math.sin(angle)]
    return vector

def setVector(vector, limit):
    vector = np.divide(vector, np.linalg.norm(vector))
    vector = np.multiply(vector, limit)
    return vector

def limitVector(vector, limit):
    if np.linalg.norm(vector) > limit:
        vector = np.divide(vector, np.linalg.norm(vector))
        vector = np.multiply(vector, limit)
    return vector

def distance(boid1, boid2):
    x = boid2.position[0] - boid1.position[0]
    y = boid2.position[1] - boid1.position[1]
    return math.sqrt(x**2 + y**2)


class BoidTemplate():
    def __init__(self, size):
        self.position = [random.randint(0,size[0]), random.randint(0,size[1])]
        self.velocity = np.array(genVec()); self.velocityLength = 0
        self.acceleration = np.array(genVec())
        self.size = 5
        self.sight = 150
        self.lookingAt = []; self.averageVelocity = np.zeros(2)
        self.maxSpeed = 5
        self.maxAcceleration = 2

    
    def randomDirection(self, multiplier):
        vector = genVec()
        vector = np.multiply(np.multiply(vector, random.random()), multiplier)
        return vector

    def seperation(self, lookingAt): #Avoid crashes
        totalVelocity = np.zeros(2)
        for boid in lookingAt:
            if distance(boid, self) != 0:
                difference = np.subtract(self.position, boid.position)
                difference = np.multiply(difference, 10/distance(boid,self)**5)
                totalVelocity = np.add(totalVelocity, difference)
        finalVelocity =  np.divide(totalVelocity, len(lookingAt))
        finalVelocity = setVector(finalVelocity, self.maxSpeed)
        finalVelocity = np.subtract(finalVelocity, self.velocity)
        finalVelocity = setVector(finalVelocity, self.maxAcceleration)
        return finalVelocity
    

    def alignment(self, lookingAt): #
        totalVelocity = np.zeros(2)
        for boid in lookingAt:
            totalVelocity = np.add(totalVelocity, boid.velocity)
        finalVelocity =  np.divide(totalVelocity, len(lookingAt))
        finalVelocity = setVector(finalVelocity, self.maxSpeed)
        finalVelocity = np.subtract(finalVelocity, self.velocity)
        finalVelocity = setVector(finalVelocity, self.maxAcceleration)
        return finalVelocity

    def cohesion(self, lookingAt): #Clump together
        totalPosition = np.zeros(2)
        for boid in lookingAt:
            totalPosition = np.add(totalPosition, boid.position)
        averagePosition =  np.divide(totalPosition, len(lookingAt))
        finalVelocity = np.subtract(averagePosition, self.position)
        finalVelocity = setVector(finalVelocity, self.maxSpeed)
        finalVelocity = np.subtract(finalVelocity, self.velocity)
        finalVelocity = setVector(finalVelocity, self.maxAcceleration)
        return finalVelocity

    


    #Defines how a boid moves
    def flock(self, boids):
        lookingAt = []
        for boid in boids:
            if distance(boid, self) <= self.sight and boid != self:
                lookingAt.append(boid)
        if len(lookingAt) > 0:
            self.acceleration = np.add(self.acceleration, np.multiply(self.seperation(lookingAt),1) )
            self.acceleration = np.add(self.acceleration, np.multiply(self.alignment(lookingAt),0.5) )
            self.acceleration = np.add(self.acceleration, np.multiply(self.cohesion(lookingAt),0.7) )
            self.acceleration = limitVector(self.acceleration, self.maxAcceleration)
        self.acceleration = np.add(self.acceleration, self.randomDirection(0.5))


    def update(self, size):
        self.velocity += self.acceleration
        self.velocity = setVector(self.velocity, self.maxSpeed)
        self.position += self.velocity
        self.position = np.mod(self.position, size)
        
    def draw(self, screen):
        #pygame.draw.line(screen, (255,0,0), self.position, np.add(self.position, setVector(self.velocity, 20)), 1)
        pygame.draw.circle(screen, (0,0,0), self.position, self.size)




def main():
    size = (1400,775)
    #****   Start Setup ****
    boids = []
    for i in range(50):
        boids.append(BoidTemplate(size))



    #****   End Setup ****
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Python Boid Sim")
    clock = pygame.time.Clock()
    done = False
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #****   Game Loop Start ****
        screen.fill((255,255,255))
        for boid in boids:
            boid.flock(boids)
        for boid in(boids):
            boid.update(size)
            boid.acceleration = np.zeros(2)
            boid.draw(screen)
            


            
        #****   Game Loop End ****

        pygame.display.flip()
        clock.tick(50)

main()