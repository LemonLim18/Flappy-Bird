import sys
import pygame
from pygame.locals import *
from pygame import mixer
import random
from tkinter import font

#functions or methods
class Button():
    def __init__(self,image,x,y,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.button_rect = self.image.get_rect() #Get the rectangle position or info for displaying use
        self.button_rect.topleft = (x,y)
        self.clickable = True
    
    """Creating a general universal button for multipurpose actions"""
    def draw(self):  
        any_action = False
        screen.blit(self.image,(self.button_rect.x,self.button_rect.y))
        #get mouse position
        mouse_pos = pygame.mouse.get_pos()
        #check if the mouse is on the button and if the button is clicked
        #[0] means left-button,[1] means middle and [2] means right-button. == 1 indicates clicked and == 0 means not clicked
        if self.button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
            if self.clickable == True:
                """LATER CHANGE TO THE INTENDED ACTION"""
                self.clickable = False  #Currently in state of unclickable
                any_action = True
            if pygame.mouse.get_pressed()[0] == 0: #Once release the left button,
                self.clickable = True #The button becomes click-able again
        return any_action

def flash_scene():
    global hitFlash
    if not hitFlash:
        flash = pygame.image.load("asset/flash.png")
        for i in range(28):
            flash.set_alpha(i)
            screen.blit(flash,(0,0))
            pygame.display.update()
        hitFlash = True

def bird_clash():
    while True:
        if bird_rect.bottom < 700:#before reaching the floor
            bird_movement += gravity
            bird_rect.centery += bird_movement
            rotated_bird = pygame.transform.rotozoom(bird_image,bird_movement*-6.2,1)
        else:
            bird_deadimage = pygame.transform.rotozoom(bird_image,-92,1)
            screen.blit(bird_deadimage,(130,690))


def draw_floor():
    screen.blit(floor_image,(floor_x ,700)) #Two screen blits are used to overlap both floor to make it seem longer,if only use the one below, the floor will only appear at behind
    screen.blit(floor_image,(floor_x + 1020,700)) #Optional coding:Used for lengthening the background

def create_pipes():
      pipe_y = random.choice(pipe_heightList)
      
      top_pipe = pipe_imageTop.get_rect(midbottom=(1000, pipe_y - 200)) #200 is the gap between top pipe and bottom pipe
      bottom_pipe = pipe_imageDown.get_rect(midtop=(1000, pipe_y))

      return top_pipe, bottom_pipe

def bird_score():
    global score 
    if bird_rect.centerx > pipe.right + 7:
        score += 1/102
        score_sound.play() 
        """Set sound once per time"""
    roundoff_score = round(score)
    score_style = pygame.font.SysFont("Comic Sans MS",60)
    score_surf = font.render(str(roundoff_score),1,(255, 128, 179)) 
    screen.blit(score_surf,((screen.get_width()/2 - score_surf.get_width()),100))

def result_page():
    final_text1 = "GAME OVER"
    final_text2 = "Your final score is "+str(round(score))
    ft1_font = pygame.font.SysFont("Arial",100) #Setting the font of the next upcoming text 
    ft1_surf = font.render(final_text1,1,(255, 153, 51)) #Turning specified string into a surface
    ft2_font = pygame.font.SysFont("Arial",50) #Swtting the font of the next upcoming text
    ft2_surf = font.render(final_text2,1,(128, 191, 255)) #Turning specified string into a surface
    screen.blit(ft1_surf,((screen.get_width()/2 - ft1_surf.get_width()/2),100)) #Display the text on the screen
    screen.blit(ft2_surf,((screen.get_width()/2 - ft2_surf.get_width()/2),200)) #Display the text on the screen
    result_birdImage = pygame.transform.rotozoom(bird_image,-58,1)
    screen.blit(result_birdImage,(120,660))
    screen.blit(floor_image,(0,700))
    pygame.display.update()
    


"""this is the main function:"""
pygame.init()

#Window
size = width,height = 900,771
screen = pygame.display.set_mode(size)
title = pygame.display.set_caption("Flappy Bird")
iconImage = pygame.image.load("asset/icon.png").convert_alpha()
icon = pygame.display.set_icon(iconImage)
clock = pygame.time.Clock()

#Font 
pygame.font.init()
font = pygame.font.SysFont(None,50)


#Sounds & Musics
mixer.init()
mixer.music.load("asset/music.mp3")
mixer.music.play()
score_sound = pygame.mixer.Sound("asset/sounds_score.wav")
score_sound.set_volume(0.06)
flap_sound = pygame.mixer.Sound("asset/sounds_wing.wav")
fall_sound = pygame.mixer.Sound("asset/sounds_die.wav")
hit_sound = pygame.mixer.Sound("asset/sounds_hit.wav")
swoosh_sound = pygame.mixer.Sound("asset/sounds_swoosh.wav")
sound_once = True

#Background
background_image = pygame.image.load("asset/background.jpg").convert()

#Floor
floor_image = pygame.image.load("asset/floor.png")
floor_image = pygame.transform.scale(floor_image, (1100,71))
floor_x = 0

#Bird
#(image)
bird_upflap = pygame.image.load("asset/yellowbird-upflap.png").convert_alpha()
bird_midflap = pygame.image.load("asset/redbird-midflap.png").convert_alpha()
bird_downflap =pygame.image.load("asset/bluebird-downflap.png").convert_alpha()
BIRDS = [bird_upflap,bird_midflap,bird_downflap]
bird_index = 0
bird_image = BIRDS[bird_index]
BIRD_FLAP = pygame.USEREVENT  #Set BIRD_FLAP as a user-defined event
pygame.time.set_timer(BIRD_FLAP,200) #Will execute an action repeatedly after a specified gap of time
#(position and space)
bird_rect = bird_image.get_rect(center=(150,771//2)) #center refers to the center point of the surface
bird_movement = 0
gravity = 0.15

#Pipes
pipe_imageDown = pygame.image.load("asset/pipe-green.png").convert_alpha()  #convert() is used to convert the pygame.Surface readily to the same pixel format as the one you use for final display
#If you don't call it, then every time you blit a surface to your display surface, a pixel conversion will be needed - this might slows down the process
#convert() is same as convert_alpha(), just that the latter supports transparency
pipe_imageTop = pygame.image.load("asset/pipe-greenTop.png").convert_alpha()
pipe_heightList = [350,400,600,533]

PIPES = [] #Create a blank list named pipes
CREATE_PIPES = pygame.USEREVENT + 1 #Create a user defined event called CREATE_PIPES
pygame.time.set_timer(CREATE_PIPES,1250) #Will call the event every 1.2 seconds
 
#Scores and result
show_FinalResult = False
score = 0
run = True

#Game over
restart_confirm = False
restart_image = pygame.image.load("asset/message.png")
restart_rect = restart_image.get_rect(center =(width//2,height//2))

#button pressed
jump_activate = True

#hit and flash
hitFlash = False

while True:
    clock.tick(125)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  #It's sys.exit(), not sys.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE and not restart_confirm and jump_activate: #Space button for jump during game
                flap_sound.play()
                bird_movement = 0       #Reset the the downward speed
                bird_movement = -6.1      #and going up (negative sign indicates upward or leftward direction)
            if event.key == K_SPACE and restart_confirm:   #Space button for start the new game
                """Reset every function or boolean statuses to their default value"""
                sound_once = True
                score = 0
                restart_confirm = False   
                hitFlash = False   #Reactivate the hit flash
                show_FinalResult = False
                jump_activate = True  #Reactivate the jump key after the restart
                PIPES = []   #empty the list
                bird_movement = 0  #reset the bird speed or movement
                bird_rect.centery = 771//2
            
        if event.type == BIRD_FLAP:
            bird_index += 1
            if bird_index > 2:
                bird_index = 0
        if event.type == CREATE_PIPES:
            PIPES.extend(create_pipes()) 

        bird_image = BIRDS[bird_index]
        """Maybe not an optional code and the latest center of surface will be determined using bird_rect.center
        and be changed from time to time, telling the computer where it supposed to be at any particular time
        .If not, the bird surface, even though reaches a certain height, but will appear to be virtual at that 
        moment"""
        bird_rect = bird_image.get_rect(center=bird_rect.center) 

    #Background
    screen.blit(background_image,(0,0))

    #Game over
    if not restart_confirm:
        #Bird-floor clash case
        if bird_rect.bottom >= 690:
            show_FinalResult = True   #是时候展示最终成绩
            pygame.time.delay(800)
            result_page() #一直重复展示最终成绩，直到按钮被点击
            pygame.time.delay(3000)
            restart_confirm = True

        #Pipes animation
        i = 1
        for pipe in PIPES: #if 1%2 == 1, i += 1  //of 
            if i % 2 == 1:
                screen.blit(pipe_imageTop,pipe)
                i += 1
            elif i % 2 == 0:
                screen.blit(pipe_imageDown,pipe) #"""Why the same item?"""
                i += 1

            pipe.centerx -= 3

            if pipe.right < 0:
                PIPES.remove(pipe) #Remove the pipes that are out of the screen
        
            #Bird-pipe clash case
            if bird_rect.colliderect(pipe): #Make it drop first
                if sound_once:
                    hit_sound.play()
                    pygame.time.delay(38)
                    fall_sound.play()
                    sound_once = False
                show_FinalResult = True
                if bird_rect.bottom >= 690:
                    pygame.time.delay(800)
                    result_page() #一直重复展示最终成绩，直到按钮被点击
                    pygame.time.delay(3000)
                    restart_confirm = True
                                

                bird_movement += gravity
                bird_rect.centery += bird_movement
                rotated_bird = pygame.transform.rotozoom(bird_image,bird_movement*-6.2, 1)
                screen.blit(rotated_bird,bird_rect)
                flash_scene()
                
                jump_activate = False       #Deactivate the jump key at this point
            
            #Bird score function call
            if not show_FinalResult: #还没展示最终成绩前，先展示目前的成绩
                bird_score()


        #Bounce off of the top side of window after a small clash
        if bird_rect.top <= 50: 
            bird_movement += 0.07
            bird_rect.centery += bird_movement
            rotated_bird = pygame.transform.rotozoom(bird_image,bird_movement*-6.2, 1)
            screen.blit(rotated_bird,bird_rect)

        
        #Bird animation
        bird_movement += gravity #Going down speed will increase by gravity(SPEED)
        bird_rect.centery += bird_movement #Speed be converted into the y-position(POSITION)
        rotated_bird = pygame.transform.rotozoom(bird_image, bird_movement*-6, 1) #Go down,tilt down; Go up, tilt up(IMAGE)
        screen.blit(rotated_bird ,bird_rect) #Display the bird at its current position(DISPLAY)
    
        
    elif restart_confirm: #later switch these two names
        screen.blit(restart_image,restart_rect)
            #Once game over, return to the main page

    #Floor(continue to move no matter what)
    floor_x -= 3 #Make the background shift to the left
    if floor_x < -700: #Once the background has shift more than 1000 to the left
        floor_x = 0  #The origin of the background will reset
    draw_floor()

    pygame.display.update()
