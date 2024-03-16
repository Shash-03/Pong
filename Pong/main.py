import pygame
import random
import math

pygame.init()

#Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#Frame rate
fps = 60
timer = pygame.time.Clock()

#global variables
wall_thickness = 10
barrier_thickness = 5
paddle_length = 60
paddle_breadth = 8
paddle_speed = 10
ball_speed = 5
score_limit = 7
deflection = 0.5
sound_effect = pygame.mixer.Sound("4143__patchen__atik-2-6-stereoatik.wav")

#font
font = pygame.font.Font(None,50)
winning_font = pygame.font.Font(None,150)

#Ball class
class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, retention, x_speed, y_speed, id,player1,player2):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.retention = retention
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.id = id
        self.circle = ''
        self.player1 = player1
        self.player2 = player2

    def draw(self):
        self.circle = pygame.draw.circle(screen,self.color, (self.x_pos,self.y_pos),self.radius)

    def move(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed

    def spawn(self):
        self.x_pos = SCREEN_WIDTH//2
        self.y_pos = SCREEN_HEIGHT//2
        self.y_speed = random.uniform(-5,5)
        if (random.random() > 0.5):
            self.x_speed = ball_speed
        else:
            self.x_speed = -1* ball_speed

    def collision(self):
        if self.x_pos <= 0: 
            return 2
        elif self.x_pos >= SCREEN_WIDTH:
            return 1
        else:
            return 0
        
    def walls(self):
        if self.y_pos <= wall_thickness or self.y_pos >= SCREEN_HEIGHT - wall_thickness:
            return True
        return False
    
    def paddle1(self):
        closest_x = max(player1.x_pos, min(self.x_pos, player1.x_pos+player1.breadth))
        closest_y = max(player1.y_pos, min(self.y_pos, player1.y_pos+player1.length))

        distance = math.sqrt((self.x_pos - closest_x) ** 2 + (self.y_pos - closest_y) ** 2)

        if distance <= self.radius:
            return True

        return False
    
    def paddle2(self):
        closest_x = max(player2.x_pos, min(self.x_pos, player2.x_pos+player2.breadth))
        closest_y = max(player2.y_pos, min(self.y_pos, player2.y_pos+player2.length))

        distance = math.sqrt((self.x_pos - closest_x) ** 2 + (self.y_pos - closest_y) ** 2)

        if distance <= self.radius:
            return True

        return False
 

#Player Class

class Player:
    def __init__(self,x_pos,y_pos,color,y_speed,length,breadth,id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.y_speed = y_speed
        self.length = length
        self.breadth = breadth
        self.id = id
        self.paddle = ""
        self.score = 0

    def draw(self):
        self.paddle = pygame.draw.rect(screen,self.color,(self.x_pos,self.y_pos,self.breadth,self.length))


#Function to draw walls at the borders
def draw_walls():
    up = pygame.draw.line(screen, "white", (0,SCREEN_HEIGHT), (SCREEN_WIDTH,SCREEN_HEIGHT),wall_thickness)
    down = pygame.draw.line(screen, "white", (0,0), (SCREEN_WIDTH,0),wall_thickness)
    walls_list = [up,down]

#Function to draw the dotted barrier in the middle
def draw_dotted_line(x_pos,y_start,y_end,length):
    counter = (y_end - y_start)//length

    for i in range(counter):
        pygame.draw.line(screen,"white",(x_pos,y_start),(x_pos,y_start + 0.9*length),barrier_thickness)
        y_start += length



run = True
#Instantiating objects

player1 = Player(40,SCREEN_HEIGHT//2,"white",paddle_speed,paddle_length,paddle_breadth,1)
player2 = Player(760,SCREEN_HEIGHT//2,"white",paddle_speed,paddle_length,paddle_breadth,2)
ball = Ball(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,5,'white',100,.9,ball_speed,0,1,player1,player2)
#main loop
while run:
    timer.tick(fps)

    screen.fill((0,0,0))

    walls = draw_walls()
    ball.draw()
    barrier = draw_dotted_line(SCREEN_WIDTH//2,0,SCREEN_HEIGHT,20)
    player1.draw()
    player2.draw()

    player_1_score = font.render(str(player1.score),True,"white")
    player_2_score = font.render(str(player2.score),True,"white")

    screen.blit(player_1_score,(SCREEN_WIDTH//2 - 45,30))
    screen.blit(player_2_score, (SCREEN_WIDTH//2 + 25, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if player1.score == score_limit or player2.score == score_limit:
        run = False

    ball.move()
    if ball.collision() == 1:
        player1.score += 1
        ball.spawn()
    
    elif ball.collision() == 2:
        player2.score += 1
        ball.spawn()

    elif ball.walls() == True :
        ball.y_speed *= -1
        sound_effect.play()

    elif ball.paddle1():
        middle = player1.y_pos + player1.length/2
        factor = ball.y_pos - middle
        ball.y_speed += factor*deflection
        ball.y_speed = max(ball.y_speed,-2.5)
        ball.y_speed = min(ball.y_speed,2.5)
        ball.x_speed *= -1
        sound_effect.play()

    elif ball.paddle2():
        middle = player2.y_pos + player2.length/2
        factor = ball.y_pos - middle
        ball.y_speed += factor*deflection
        ball.y_speed = max(ball.y_speed,-2.5)
        ball.y_speed = min(ball.y_speed,2.5)
        ball.x_speed *= -1
        sound_effect.play()
        
    keys = pygame.key.get_pressed()

    

    if keys[pygame.K_w]:
        if player1.y_pos - player1.y_speed >= wall_thickness:
            player1.y_pos -= player1.y_speed

    elif keys[pygame.K_s]:
        if player1.y_pos + player1.y_speed + player1.length <= SCREEN_HEIGHT - wall_thickness:
            player1.y_pos += player1.y_speed
    

    elif keys[pygame.K_UP]:
        if player2.y_pos - player2.y_speed >= wall_thickness:
            player2.y_pos -= player2.y_speed

    elif keys[pygame.K_DOWN]:
        if player2.y_pos + player2.y_speed + player2.length <= SCREEN_HEIGHT - wall_thickness:
            player2.y_pos += player2.y_speed

    ball.x_speed *= 1.0005
    
    
    pygame.display.update()

if player1.score == score_limit or player2.score == score_limit:
    runner = True
else:
    runner = False
while runner:
    if player1.score == score_limit:
        winner = winning_font.render("Player 1 wins",True,"white")
        screen.blit(winner,(40,SCREEN_HEIGHT//2))
    else:
        winner = winning_font.render("Player 2 wins",True,"white")
        screen.blit(winner,(40,SCREEN_HEIGHT//2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False

    pygame.display.update()


    

        
