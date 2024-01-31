import socket
import pygame
import pickle
from button import Button
from cherry import Cherry
from plate import Plate

# Socket settings
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # setting the socket
my_socket.connect(('127.0.0.1', 1024)) # joining the server

# Constants
Width = 1200
Height = 675

# Screen Init
pygame.init()
size = (Width, Height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catch the Cherry - Player 2") # Name for player 2
clock = pygame.time.Clock()

# Background
background = pygame.image.load("Untitled-2.png")
screen.blit(background, (0, 0))
pygame.display.update()

# Cherrys and Buttons
cherry1_image = pygame.image.load("b.png") # Player 1's berry
player1_image = pygame.image.load("Plate.png") # Player 1's plate
cherry2_image = pygame.image.load("a.png") # Player 2's berry
player2_image = pygame.image.load("Plate2.png") # Player 2's plate
Player2 = Plate(850, screen, player2_image) # Settings of the player
C2 = Cherry(2, screen, cherry2_image) # Setting of the cherry
yes_button = Button(381, 270, 100, 200, (0, 255, 0), (255, 0, 0), screen, "Yes", (0, 0, 0), 50)
no_button = Button(591, 270, 100, 200, (0, 255, 0), (255, 0, 0), screen, "No", (0, 0, 0), 50)

# Audios
game_music = pygame.mixer.Sound("game_music.mp3")
game_music.set_volume(0.05)
speed_up = pygame.mixer.Sound("speedup.mp3")
speed_up.set_volume(0.2)
catch_sound = pygame.mixer.Sound("catch.mp3")
catch_sound.set_volume(0.2)
damage_sound = pygame.mixer.Sound("damage.mp3")
damage_sound.set_volume(0.2)

finish = False
pressed = False
pressed1 = False
frame_0 = True
score = 0
player2_choice = 0
player1_choice = 0

# defs
def show_player(): # shows text which player you are
    font = pygame.font.Font('freesansbold.ttf', 40)
    text_score = font.render("Player 2", False, (0, 0, 0))
    screen.blit(text_score, (15, 25))
def show_hp(): # shows text with your current hp
    font = pygame.font.Font('freesansbold.ttf', 40)
    text_score = font.render("Hp: " + str(Player2.hp), False, (0, 0, 0))
    screen.blit(text_score, (15, 75))
def show_score(): # shows text with your current score
    font = pygame.font.Font('freesansbold.ttf', 40)
    text_score = font.render("Score: " + str(Player2.score), False, (0, 0, 0))
    screen.blit(text_score, (15, 125))

while not finish: # when the player or the other player didn't exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
    try: # check if both of the players are ingame
        if frame_0: # if the game just started
            game_music.play()
            frame_0 = False
        x1, hp, score, Cx2, Cy2, player1_choice, pressed1 = pickle.loads(my_socket.recv(1024)) # Getting data from the server
        my_socket.send(pickle.dumps([Player2.x, Player2.hp, Player2.score, C2.x, C2.y, player2_choice, pressed])) # Sending data to the server
        Player1 = Plate(x1, screen, player1_image) # Setting the other player's data according the server's data
        Player1.hp = hp # Setting the other player's hp according the server's data
        Player1.score = score # Setting the other player's score according the server's data
        C1 = Cherry(1, screen, cherry1_image) # Setting the other cherry's data according the server's data
        C1.x = Cx2 # Setting the other cherry's x according the server's data
        C1.y = Cy2 # Setting the other cherry's y according the server's data
        screen.blit(background, (0, 0))
        pygame.draw.line(screen, (0, 0, 0), ((Width/2 - 15), Height), ((Width/2 - 15), 0), 10) # Showing the middle line between the players arenas
        Player1.show() # showing the player 1's model
        Player2.show() # showing the player 2's model
        show_player() # Showing the player's number
        show_score() # Showing the player's score
        show_hp() # Showing the player's hp
        if Player1.hp > 1 and Player2.hp > 1: # If the players didn't lose the game yet
            C1.show() # showing the player 1's cherry model
            C2.show() # showing the player 2's cherry model
        else:
            game_music.stop()
            if not pressed: # Shows the restart option button when the user didn't press on any button
                C2.v = 0
                font = pygame.font.Font('freesansbold.ttf', 55)
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(222, 140, 750, 75))
                text_score = font.render("Do you want to play again?", False, (255, 255, 255))
                screen.blit(text_score, (234, 150))
                yes_button.draw()  # showing the button yes
                if yes_button.is_pressed():  # checking if the user pressed on the button yes
                    pressed = True
                    player2_choice = 1
                no_button.draw()  # showing the button no
                if no_button.is_pressed():  # checking if the user pressed on the button no
                    pressed = True
                    player2_choice = 0
            elif pressed and pressed1: # if both of the players have pressed
                if player1_choice == 1 and player2_choice == 1: # if both of the players pressed yes then it'll restart the game
                    Player2 = Plate(850, screen, player2_image) # Settings of the player
                    C2 = Cherry(2, screen, cherry2_image) # Setting of the cherry
                    pressed = False
                    player1_choice = 0
                    player2_choice = 0
                    frame_0 = True
                else: # if not all the players pressed yes
                    font = pygame.font.Font('freesansbold.ttf', 55)
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(222, 140, 750, 75))
                    text_score = font.render("Game Over, press x to exit", False, (255, 255, 255))
                    screen.blit(text_score, (234, 150))
            elif pressed and not pressed1: # if the player pressed and the other player didn't
                font = pygame.font.Font('freesansbold.ttf', 55)
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(222, 140, 800, 75))
                text_score = font.render("Waiting for the other player...", False, (255, 255, 255))
                screen.blit(text_score, (232, 150))
            if Player1.hp > 1 and Player2.hp == 1:  # if player1 won
                font = pygame.font.Font('freesansbold.ttf', 60)
                Won = font.render("Player 1 Won", False, (255, 255, 255))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(383, 72, 400, 75))
                screen.blit(Won, (392, 80))
            elif Player2.hp > 1 and Player1.hp == 1:  # if player2 won
                font = pygame.font.Font('freesansbold.ttf', 60)
                Won = font.render("Player 2 Won", False, (255, 255, 255))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(383, 72, 400, 75))
                screen.blit(Won, (390, 80))
            else:  # if they both lost in the same time and finished with 1 hp
                font = pygame.font.Font('freesansbold.ttf', 60)
                Tie = font.render("Tie", False, (255, 255, 255))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(532, 50, 110, 75))
                screen.blit(Tie, (541, 60))

        keys = pygame.key.get_pressed() # getting the user's key input

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: # if the player pressed on d or right key it'll move the player right
            if Player2.x < 1195: # moving the player left if he isn't on the border
                Player2.move(1)
            else:
                Player2.x = 590

        elif keys[pygame.K_a] or keys[pygame.K_LEFT]: # if the player pressed on a or left key it'll move the player left
            if Player2.x > 598: # moving the player right if he isn't on the border
                Player2.move(-1)
            else:
                Player2.x = 1170

        elif keys[pygame.K_x]: # if the player pressed on x it'll close the game
            finish = True

        C2.move() # moving the cherry down

        if Player2.Hit(C2): # if the player hits the berry it adding 10 score
            catch_sound.play()
            Player2.score += 10
            if Player2.score % 150 == 0:  # if the player's score is divided by 150 the cherry's speed will be faster
                C2.v += 10
            if Player2.score % 200 == 0:  # if the player's score is divided by 200 the player's speed will be faster
                Player2.v += 0.25
                speed_up.play()
            C2 = Cherry(2, screen, cherry2_image)

        elif C2.y >= 580: # if the player doesn't hit the berry its removing him 10 hp if he has more then 10 hp
            damage_sound.play()
            if Player2.hp > 10:
                Player2.hp -= 10
            else:
                Player2.hp -= 9
            C2 = Cherry(2, screen, cherry2_image) # creating a new berry which spawns up
    except:
        my_socket.close()
        screen.blit(background, (0, 0))
        font = pygame.font.Font('freesansbold.ttf', 60)
        Left = font.render("The other player left the game", False, (0, 0, 0))
        screen.blit(Left, (160, 200))
        Left2 = font.render("press x to exit", False, (0, 0, 0))
        screen.blit(Left2, (375, 280))
        keys = pygame.key.get_pressed()  # getting the user's key input
        if keys[pygame.K_x]: # if the player pressed on x it'll close the game
            finish = True

    pygame.display.update()
    clock.tick(60)