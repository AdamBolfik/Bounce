'''
Created on Oct 2, 2013

@author: adam
'''
#! /usr/bin/python
import pygame, math
from random import randint
from pygame.locals import *
from sys import exit

SCREEN_SIZE = (800, 600)
BALL_SPEED = 1
LINE_SPEED = 1
HORIZONTAL = 1 
VERTICAL = 0
# CHANGE SPEED AND COLOR IN QUADRANTS
pygame.init()

def main():
    global SCREEN_SIZE 
    global HORIZONTAL 
    global VERTICAL
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]), 0, 32)
    pygame.display.set_caption("Balls!!") 
    
    expanding_line, line_list, ball_list, box_list = [], [], [], []
    num_balls = 5
    
    while num_balls:
        ball_list.append(Ball(randint(0, SCREEN_SIZE[0]), randint(0, SCREEN_SIZE[1])))
        num_balls = num_balls -1  
    
    box_list.append(Box(0, 0, 800, 600))
    
    while True:
        time_passed = clock.tick(300) # Maximum of 60 FPS
        time_passed_seconds = time_passed / 1000.0      
        screen.fill((161, 77, 80)) # Make background color gray 
        for event in pygame.event.get():
            lmb, mmb, rmb = pygame.mouse.get_pressed()
            m_x, m_y = pygame.mouse.get_pos()            
            if event.type == QUIT: # If user closes window, game will exit 
                exit()
            if lmb:
                if len(expanding_line) == 0:
                    expanding_line.append(Line(m_x, m_y, HORIZONTAL))
            if rmb:
                if len(expanding_line) == 0:
                    expanding_line.append(Line(m_x, m_y, VERTICAL))
        
        
        
        pygame.draw.rect(screen, (50, 60, 70), [200, 200, 100, 100])
        pygame.display.update() # Redraws the components on the screen     

class Box():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.length = y2 - y1
        self.width = x2 - x1
        self.area = (x2 - x1) * (y2 - y1)
    def in_box(self, pt):
        if(pt[0] > self.x1 and pt[0] < self.x2)and(pt[1] > self.y1 and pt[1] < self.y2):
            return True
        else:
            return False
    def is_empty(self, balls):
        is_empty = False
        for b in balls:
            if self.in_box(b.pt):
                is_empty = True
        return is_empty

class Line():
    global SCREEN_SIZE 
    def __init__(self, x, y, orientation):
        self.pt = (x, y)
        self.x_beg = x  
        self.y_beg = y
        self.x_end = x
        self.y_end = y        
        self.orientation = orientation # HORIZONTAL(1) or VERTICAL(0)    
        # The line has reached both ends of the screen
        self.fin_beg = False 
        self.fin_end = False

    def expand_line(self, lines): # Checks if line has reached the edge, increments if not               
#         if not self.fin_beg:        # If right side has not ended
#             if self.orientation:    # If horizontal
#                 if self.x_beg < SCREEN_SIZE[0]:                
#                     self.x_beg += 1
#                 else:
#                     self.fin_beg = True
#             if not self.orientation:
#                 if self.y_beg < SCREEN_SIZE[1]:
#                     self.y_beg += 1 
#                 else:
#                     self.fin_beg = True
#         if not self.fin_end:
#             if self.orientation:
#                 if self.x_end > 0:
#                     self.x_end -= 1
#                 else:
#                     self.fin_end = True
#             if not self.orientation:
#                 if self.y_end > 0:
#                     self.y_end -= 1 
#                 else:
#                     self.fin_end = True
                    
        for l in lines:
            if self.orientation:
                if self.x_beg == l.x_beg:
                    if self.y_beg <= l.y_beg and self.y_beg >= l.y_end:
                        self.fin_beg = True
                if self.x_end == l.x_beg:
                    if self.y_end <= l.y_beg and self.y_end >= l.y_end:
                        self.fin_end = True
            if not self.orientation:
                if self.y_beg == l.y_beg:
                    if self.x_beg <= l.x_beg and self.x_beg >= l.x_end:
                        self.fin_beg = True
                if self.y_end == l.y_beg:
                    if self.x_end <= l.x_beg and self.x_end >= l.x_end:
                        self.fin_end = True
                    
class Ball():
    global SCREEN_SIZE 
    global BALL_SPEED
    def __init__(self, x, y):
        self.pt = (x, y)
        self.x = x
        self.y = y
        # Ball color currently set to Blue - RGB (0-255, 0-255, 0-255)
        self.color = (0, 150, 220)          
        self.radius = 10
        # How much a ball is incremented each time update_pos() is called
        self.x_vel = BALL_SPEED                       
        self.y_vel = BALL_SPEED                      
    # Increments ball position
    def update_pos(self): 
        # Check if it has hit edges of screen 
        # and reverses ball direction accordingly
        if(self.x <= 0):                    
            self.x = 0                     
            self.x_vel = -self.x_vel
        elif(self.x >= SCREEN_SIZE[0] - (self.radius / 2)):
            self.x = SCREEN_SIZE[0] - (self.radius / 2)
            self.x_vel = -self.x_vel
        elif(self.y <= 0 + (self.radius / 2)):
            self.y = 0 + (self.radius / 2)
            self.y_vel = -self.y_vel
        elif(self.y >= SCREEN_SIZE[1] - (self.radius / 2)):
            self.y = SCREEN_SIZE[1] - (self.radius / 2)
            self.y_vel = -self.y_vel
        self.x += self.x_vel
        self.y += self.y_vel
    # Checks if the ball has hit another ball
    def hit_ball(self, b2):                 
        # Calculate distance of one ball to another
        distance = math.sqrt(((self.x - b2.x)** 2) + ((self.y - b2.y)** 2)); 
        # Compare distance to sum of radii
        if(distance <= self.radius + b2.radius):        
            # Adjust accordingly if the balls hit
            if((self.x_vel < 0 and b2.x_vel > 0) or     
               (self.x_vel > 0 and b2.x_vel < 0)):
                self.x_vel = -self.x_vel
                b2.x_vel = -b2.x_vel
            if((self.y_vel < 0 and b2.y_vel > 0) or
               (self.y_vel > 0 and b2.y_vel < 0)):
                self.y_vel = -self.y_vel
                b2.y_vel = -b2.y_vel 
    # Checks if ball has hit a line
    def hit_line(self, lines):  
        hit = False 
        for line in lines:
            # HORIZONTAL
            if line.orientation:    
                if (((self.y + self.radius) == line.y_beg) and  
                    (self.x >= line.x_end and self.x <= line.x_beg)):
                    # Adjusts accordingly
                    self.y_vel = -self.y_vel    
                    hit = True    
                elif(((self.y - self.radius) == line.y_beg) and
                     (self.x >= line.x_end and self.x <= line.x_beg)):
                    self.y_vel = -self.y_vel
                    hit = True  
            # VERTICAL
            else:
                if (((self.x + self.radius) == line.x_beg) and
                    (self.y >= line.y_end and self.y <= line.y_beg)):
                    self.x_vel = -self.x_vel
                    hit = True  
                elif (((self.x - self.radius) == line.x_beg) and
                      (self.y >= line.y_end and self.y <= line.y_beg)):
                    self.x_vel = -self.x_vel
                    hit = True  
        return hit
    def get_pt(self):
        return (self.x, self.y)

if __name__ == '__main__':
    main()