#! /usr/bin/python
'''
Author: Adam Bolfik
Ver: 12.5
Date: 10/12/13
Description: Try to trap some balls...
'''
import pygame, math, decimal
from random import randint
from pygame.locals import *
from sys import exit

SCREEN_SIZE = (800, 600)    # Just what it says -- 
BALL_SPEED = 1
LINE_SPEED = 1
HORIZONTAL = 1  # Constant for lines
VERTICAL = 0    # Constant for lines

pygame.init()

def main():
    global SCREEN_SIZE 
    global HORIZONTAL 
    global VERTICAL
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]), 0, 32)
    pygame.display.set_caption("Bounce!!") 
    myfont = pygame.font.SysFont("monospace", 15)
    
    level = 1   # Initialize level
    won = False 
    play = False
    lifes = 3
    
    # Print instructions on a blank screen
    to_win = "To win: Cover 80% of area."
    to_lose = "Don't let a ball touch an expanding line"
    left_click = "Left Click: Horizontal line"
    right_click = "Right Click: Vertical line"
    spc = "Space: Reset"
    author = "Author: Adam Bolfik"
    label = myfont.render(to_win, 1, (255,255,0))
    screen.blit(label, (10, 10))
    label = myfont.render(to_lose, 1, (255,255,0))
    screen.blit(label, (10, 30))
    label = myfont.render(left_click, 1, (255,255,0))
    screen.blit(label, (10, 50))
    label = myfont.render(right_click, 1, (255,255,0))
    screen.blit(label, (10, 70))
    label = myfont.render(spc, 1, (255,255,0))
    screen.blit(label, (10, 90))
    label = myfont.render(author, 1, (0, 0, 255))
    screen.blit(label, (10, 110))
    pygame.display.update()
            
    while True:
        for event in pygame.event.get():    # Grab events from user input
            if event.type == QUIT:          # Exit game if the user closes the window
                exit()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_ESCAPE]:          # Exit game if user hits escape key 
            exit()
        if pressed_keys[K_SPACE]:           # Resets the game if won = false, next level if won = true
            if not won:
				if lifes > 0:
					lifes = lifes - 1
				else:
                  	level = 1
                    lifes = 3
            won = False
            play = True
            
        expanding_line, line_list, ball_list, box_list = [], [], [], [] # Initiialize all the lists used
        for i in xrange(level):                                         # The number of balls = level number
            ball_list.append(Ball(randint(0, SCREEN_SIZE[0]), randint(0, SCREEN_SIZE[1])))

        box_list.append(Box(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))    # Create the first box object to be the size of the screen

        while(play):    # The game will not start until the user hits space key
            time_passed = clock.tick(300) # Maximum FPS allowed
            time_passed_seconds = time_passed / 1000.0      
            screen.fill((161, 77, 80)) # Set background color
            for event in pygame.event.get():           
                if event.type == QUIT: 
                    exit()
            lmb, mmb, rmb = pygame.mouse.get_pressed()  # Store which mouse button was clicked
            pressed_keys = pygame.key.get_pressed()     # Store the keys that were pressed
            m_x, m_y = pygame.mouse.get_pos()           # Store the mouse position
            if pressed_keys[K_ESCAPE]:
                exit()
            if lmb:         # If the left mouse button was clicked, create a horizontal line
                if len(expanding_line) == 0:
                    expanding_line.append(Line(m_x, m_y, HORIZONTAL))
            if rmb:         # If the right mouse button was clicked, create a vertical line
                if len(expanding_line) == 0:
                    expanding_line.append(Line(m_x, m_y, VERTICAL))
                       
            if len(expanding_line) > 0:     # If there is a line that has not finished expanding
                for line in expanding_line:
                    if line.fin_beg and line.fin_end:   # If it finished since last time
                        line_list.append(line)          # add it to the list of lines
                        for box in box_list:            # and create two new box objects by
                            if box.in_box(line.pt):     # dividing and removing the box from
                                pt = line.pt            # which the point originated from
                                if (line.orientation):  # If the line was horizontal, divide top and bottom
                                    box_list.append(Box(box.x1, box.y1, box.x2, pt[1]))
                                    box_list.append(Box(box.x1, pt[1], box.x2, box.y2))
                                else:                   # If the line was vertical, divide left and right
                                    box_list.append(Box(box.x1, box.y1, pt[0], box.y2))
                                    box_list.append(Box(pt[0], box.y1, box.x2, box.y2))
                                box_list.remove(box)
                        expanding_line.remove(line)     
                    else:
                        line.expand_line(line_list) # Increase the length of the line until complete 
                        pygame.draw.line(screen, (50, 60, 70), (line.x_beg, line.y_beg), 
                                         (line.x_end, line.y_end), 3)
            area = 0    # reset the area to 0 so that it is not cummulatively adding
            for box in box_list:
                if box.is_empty(ball_list):     # Check if the box has any balls in it
                    pygame.draw.rect(screen, (50, 60, 70), [box.x1, box.y1, box.width, box.length]) # If empty, color box
                    area = area + box.area     # and add area of boxes
                    
            for l in line_list:     # Draw each line on the screen
                pygame.draw.line(screen, (50, 60, 70), (l.x_beg, l.y_beg), (l.x_end, l.y_end), 3)
            
            for b in ball_list:     
                b.update_pos() # Update (move) the position of the ball
                b.hit_line(line_list) # Checks if ball has hit a line 
                if(b.hit_line(expanding_line)):
                    play = False
                for n in ball_list:
                    if n is not b: # If the ball is not itself        
                        b.hit_ball(n) # Check if it has hit another ball                                
                pygame.draw.circle(screen, (20, 20, 20), (b.x - 1, b.y + 1), b.radius) # Shadow
                pygame.draw.circle(screen, b.color, (b.x, b.y), b.radius) # Ball
            
            # Print out the percent of area covered
            decimal.getcontext().prec = 2
            area_covered = (decimal.Decimal(area) / decimal.Decimal(SCREEN_SIZE[0] * SCREEN_SIZE[1])) * 100
            percent = "Percent: " + str(area_covered)
            label = myfont.render(percent, 1, (255,255,0))
            screen.blit(label, (10, 10))
            
            # If the area is over 80% the player has won, if not - continue
            if(area_covered >= 80):
                won = True
                play = False
                level = level + 1
                lifes = 3
            
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
        if(pt[0] > self.x1 and pt[0] < self.x2):
            if (pt[1] > self.y1 and pt[1] < self.y2):
                return True
        else:
            return False
    def is_empty(self, balls):
        is_empty = True
        for b in balls:
            if self.in_box((b.x, b.y)):
                is_empty = False
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
        if not self.fin_beg:        # If right side has not ended
            if self.orientation:    # If horizontal
                if self.x_beg < SCREEN_SIZE[0]:                
                    self.x_beg += 1
                else:
                    self.fin_beg = True
            if not self.orientation:
                if self.y_beg < SCREEN_SIZE[1]:
                    self.y_beg += 1 
                else:
                    self.fin_beg = True
        if not self.fin_end:
            if self.orientation:
                if self.x_end > 0:
                    self.x_end -= 1
                else:
                    self.fin_end = True
            if not self.orientation:
                if self.y_end > 0:
                    self.y_end -= 1 
                else:
                    self.fin_end = True
                    
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
        if(self.x <= 0 + (self.radius / 2)):                    
            self.x = 0 + (self.radius / 2)                   
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
