import pygame
import time 
import random 
from pygame.locals import *
from pygame import mixer

snake_speed = 18 
window_size = 400 
score = 0 

#Colors 
background_color = pygame.Color(239,242,237)
gameover_color = pygame.Color(23,23,23)
gameover_font_color = pygame.Color(237,236,235)
snake_color = pygame.Color(55,166,73)
food_color = pygame.Color(207,65,52)


#Initilize game 
pygame.init()

pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((window_size, window_size))

fps = pygame.time.Clock()

snake_position = [100,50]

snake_body = [
    [100, 50],
    [90, 50],
    [80,50],
    [70,50]
]

food_position = [
    random.randrange(1,(window_size//10)) * 10,
    random.randrange(1,(window_size//10)) * 10 
]

food_spawn = True 

direction = 'RIGHT'
change_direction = direction 




# Display score
def show_score(choice,color,font,size):

    score_font = pygame.font.SysFont(font,size)
    score_surface = score_font.render('Score :' + str(score), True, color)

    score_box = score_surface.get_rect()

    game_window.blit(score_surface,score_box)

#WORK IN PROGRESS. TRYING TO MAKE A RESTART. 
# Only "no" works at this point, but will be adding to restart the game. 
def play_again(font):
    
    playagain_surface = font.render('Play again? No - n',True, gameover_font_color )
    playagain_box = playagain_surface.get_rect()
    playagain_box.midtop = (window_size/2,window_size/2)

    game_window.blit(playagain_surface, playagain_box)
    pygame.display.flip()

    #clear up events to get to user input 
    pygame.event.clear()
    mixer.music.load('lose.mp3')
    mixer.music.play()
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                #User Quits 
                if event.key == pygame.K_n:
                    pygame.quit()
                    quit()


                #Work in progress 
                elif event.key == pygame.K_y:
                    # something to restart

                    # snake_position = [100,50]

                    # snake_body = [
                    #     [100, 50],
                    #     [90, 50],
                    #     [80,50],
                    #     [70,50]
                    # ]

                    # food_position = [
                    #     random.randrange(1,(window_size//10)) * 10,
                    #     random.randrange(1,(window_size//10)) * 10 
                    # ]
                    pygame.quit()
                    quit()

    


#game over 
def game_over(): 

    mixer.music.stop()
    font = pygame.font.SysFont('arial',20)

    gameover_surface = font.render('Your Score is: ' + str(score), True, gameover_font_color )
    gameover_box = gameover_surface.get_rect()
  

    gameover_box.midtop = (window_size/2,window_size/4)

    game_window.fill(gameover_color)
    game_window.blit(gameover_surface, gameover_box)
    

    play_again(font)



#Main 
mixer.init()
mixer.music.load('factory_time.mp3')
mixer.music.play()
while True: 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_UP:
                change_direction = 'UP'
            if event.key == pygame.K_DOWN:
                change_direction = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_direction = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_direction = 'RIGHT'

    #Making sure the snake doesn't move in 2 directions when 2 keys are pressed simulatneously.
    if change_direction == 'UP' and direction != 'DOWN': 
        direction = 'UP'
    if change_direction == 'DOWN' and direction != 'UP': 
        direction = 'DOWN'
    if change_direction == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_direction == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    
    #Move snek 

    if direction == 'UP':
        snake_position[1] -= 10 
    if direction == 'DOWN':
        snake_position[1] += 10 
    if direction == 'LEFT':
        snake_position[0] -= 10 
    if direction == 'RIGHT':
        snake_position[0] += 10 


    #Growing snake's body 

    snake_body.insert(0,list(snake_position))
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 10 
        food_spawn = False 
    else: 
        snake_body.pop()

    #Food eaten, generate new food 
    if not food_spawn:
        food_position = [random.randrange(1,(window_size//10)) * 10,
                random.randrange(1,(window_size//10)) * 10 ]
    
    food_spawn = True 

    game_window.fill(background_color)

    for pos in snake_body:
        pygame.draw.rect(game_window,snake_color,pygame.Rect(
            pos[0],pos[1],10,10)
        )

    pygame.draw.rect(game_window,food_color,pygame.Rect(

        food_position[0],food_position[1],10,10)
    )

    #Game over
    if snake_position[0] < 0 or snake_position[0] > window_size -10: 
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_size - 10: 
        game_over()

    #body touched
    for block in snake_body[1:]: 
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
    
    show_score(1,gameover_color,'arial', 20)

    pygame.display.update()

    fps.tick(snake_speed)
