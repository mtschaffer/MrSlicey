import sys
import os
import pygame
import random

#Rules:
#1) Worked on in your free time
#2) Can't remove other contributors' features
#3) You can add a single feature on your turn
#4) Feature must make the game "more fun"

class Watermelon:
    
    #Load the watermelon image and stick it in the middle of the screen
    def __init__(self):
        self.image = pygame.image.load(os.path.join('images', 'watermelon.png')).convert_alpha()
        self.x = 320
        self.y = 240
        
        self.move_speed = 4.0
        self.move_x = 0
        self.move_y = 0
    
    #Read the keystate so we can move
    def input(self, keystate):
        self.move_x = 0
        if keystate[pygame.K_LEFT]:
            self.move_x = -self.move_speed
        elif keystate[pygame.K_RIGHT]:
            self.move_x = self.move_speed
            
        self.move_y = 0
        if keystate[pygame.K_UP]:
            self.move_y = -self.move_speed
        elif keystate[pygame.K_DOWN]:
            self.move_y = self.move_speed

    #Move the watermelon
    def update(self, lag_scalar):
        self.x = self.x + self.move_x * lag_scalar 
        self.y = self.y + self.move_y * lag_scalar 

    #Draw the watermelon        
    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y), 32, 32), (0, 0, 32, 32))

def main():
    pygame.init()

    #Game clock used for framerate calculations
    clock = pygame.time.Clock()

    #VGA resolution sounds about right
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))

    #Let's aim for 30 frames/second
    fps = 30
    
    #Our hero
    watermelon = Watermelon()
    
    #Ideally at 30 fps, each frame should take 33.3ms however this is not guarenteed
    #This scalar is updated every loop to help scale movement to allow smooth movement
    #when the time between frames is not always consistent
    lag_scalar = 1.0
    
    while (True):

        #Get the complete keyboard state
        keystate = pygame.key.get_pressed()
        
        #Send the keyboard input so our hero can react
        watermelon.input(keystate)
        
        alt_held = keystate[pygame.K_LALT] or keystate[pygame.K_RALT]
        ctrl_held = keystate[pygame.K_LCTRL] or keystate[pygame.K_RCTRL]
        
        #Read some key events to see if we need to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

        #Update our player and objects
        watermelon.update(lag_scalar)

        #Start drawing this frame by painting the whole thing black
        screen.fill((0, 0, 0))

        #Draw our player
        watermelon.draw(screen)
        
        #Show the buffer we just drew everything to and calculate the lag
        pygame.display.flip()
        msElapsed = clock.tick(fps)
        lag_scalar = msElapsed * fps / 1000.0

main()