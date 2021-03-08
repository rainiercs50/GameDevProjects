# Creater : 
# Rainier Hardjanto 

import pygame 
from random import randint 
pygame.init()

#width and height of window 
win = pygame.display.set_mode((500, 500))

#title
pygame.display.set_caption("First Game")

fl = '/Users/rainierhardjanto/Desktop/gi/Game/'

score = 0
bulletSound = pygame.mixer.Sound(fl+'bullet.mp3')
hitSound = pygame.mixer.Sound(fl+'hit.mp3')
music = pygame.mixer.music.load(fl+'music.mp3')

pygame.mixer.music.play(-1)

# -1 for the music to play forever 


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y 
        self.width = width 
        self.height = height 
        self.vel = 5
        self.isJump = False 
        self.jumpCount = 10
        self.left = False 
        self.right = False 
        self.walkCount = 0
        self.standing = True 
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) 
        #represents a rectangle (x, y, width and height)

    def draw(self, win):
      
        if self.walkCount + 1 >= 27:
            #we have 9 sprites 
            # #each sprite should be 3 frames -> 9 * 3
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            # win.blit(char, (self.x, self.y))
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)        
        #for pygame.draw.rect : if we leave the last parameter "2" blank then it will fully color it
        #if not then as we increase the value it will make the lines more thick 
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        # ensure variables are reset 
        self.isJump = False 
        self.jumpCount = 10
        self.x = 60
        self.y = 410 
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))

        #place the text in the middle 
        win.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()

        i = 0
        while i < 300:
            # completely pauses the screen 
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
        


class projectile(object):
    #bullet 
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y 
        self.radius = radius 
        self.color = color 
        self.facing = facing 
        self.vel = 8 * facing 

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

        


class enemy(object):
    walkRight = [pygame.image.load(fl+'R1E.png'), pygame.image.load(fl+'R2E.png'), pygame.image.load(fl+'R3E.png'), pygame.image.load(fl+'R4E.png'), pygame.image.load(fl+'R5E.png'), pygame.image.load(fl+'R6E.png'), pygame.image.load(fl+'R7E.png'), pygame.image.load(fl+'R8E.png'), pygame.image.load(fl+'R9E.png'), pygame.image.load(fl+'R10E.png'), pygame.image.load(fl+'R11E.png')]
    walkLeft = [pygame.image.load(fl+'L1E.png'), pygame.image.load(fl+'L2E.png'), pygame.image.load(fl+'L3E.png'), pygame.image.load(fl+'L4E.png'), pygame.image.load(fl+'L5E.png'), pygame.image.load(fl+'L6E.png'), pygame.image.load(fl+'L7E.png'), pygame.image.load(fl+'L8E.png'), pygame.image.load(fl+'L9E.png'), pygame.image.load(fl+'L10E.png'), pygame.image.load(fl+'L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.end = end 
        # counting sprites / image we are on
        self.walkCount = 0
        self.vel = 3
        # represents start and end point 
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10 
        self.visible = True
        
   
    
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                # 11 * 3 frames 
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))

            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 5 * self.health, 10))
            # 50 - (5 * (10 - self.health)) = 5 * self.health 
            # if self.health = 0 then it would be 50. Else it would decrease 

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
     


    def move(self):
        if self.vel > 0:
            #moving right 
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0

        else:
            #moving left
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False 
        

    
# animations 
walkRight = [pygame.image.load(fl+'R1.png'), pygame.image.load(fl+'R2.png'), pygame.image.load(fl+'R3.png'), pygame.image.load(fl+'R4.png'), pygame.image.load(fl+'R5.png'), pygame.image.load(fl+'R6.png'), pygame.image.load(fl+'R7.png'), pygame.image.load(fl+'R8.png'), pygame.image.load(fl+'R9.png')]
walkLeft = [pygame.image.load(fl+'L1.png'), pygame.image.load(fl+'L2.png'), pygame.image.load(fl+'L3.png'), pygame.image.load(fl+'L4.png'), pygame.image.load(fl+'L5.png'), pygame.image.load(fl+'L6.png'), pygame.image.load(fl+'L7.png'), pygame.image.load(fl+'L8.png'), pygame.image.load(fl+'L9.png')]
bg = pygame.image.load(fl+'bg.jpg')
char = pygame.image.load(fl+'standing.png')
clock = pygame.time.Clock()
#change fps 



def redrawGameWindow():
    # win.fill((0, 0, 0)) -> fills the screen with a color 
    win.blit(bg, (0, 0))
    # blit take in an X and a Y
    # pygame.draw.rect(win, (255, 0, 0), (x, y, width, height)) -> draws a rectangle 
    man.draw(win)
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (300, 10))

    # will render new text 
    

    for bullet in bullets:
        bullet.draw(win)
    for goblin in goblins:
        goblin.draw(win)



    pygame.display.update()

run = True 
man = player(300, 410, 64, 64)

goblins = []


shootLoop = 0
goblinSpawnTime = 0
bullets = []
#containing all bullets 
font = pygame.font.SysFont('comicsans', 30, True, True)
# name font, how big it is, whether its bold, whether it is italicized 



while run:
    clock.tick(27)
    #frame rate / fps / pictures every second

    for goblin in goblins:
        assert(goblin.visible == True)
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
                goblins.pop(goblins.index(goblin))
                break


    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 5:
        shootLoop = 0
    for event in pygame.event.get():
        #list of events 
        if event.type == pygame.QUIT:
            run = False 


    for bullet in bullets:
        for goblin in goblins:

            #check if we are above bottom of rectangle AND if we are below the top of our rectangle
            #check if we are on the right side of the left side of the rectangle AND we are on the left side of the right side of the rectangle
            gone = False 
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                    gone = True 
                    break

            if gone:
                break
            
            if bullet.x < 500 and bullet.x > 0:
                #not going of the screen 
                bullet.x += bullet.vel
            else:
                #find the index of the bullet then remove it 
                have = False 
                for bulleT in bullets:
                    if bulleT == bullet:
                        have = True
        
                if have:
                    bullets.pop(bullets.index(bullet))
             
    for goblin in goblins:
        if goblin.visible == False:
            goblins.pop(goblins.index(goblin))
            goblinSpawnTime = 20
           

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
             #make sure bullet is coming from the right side / left side of the man 
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
        shootLoop = 1


    if keys[pygame.K_LEFT] and man.x > man.vel: 
        man.x -= man.vel 
        man.left = True 
        man.right = False 
        man.standing = False 

    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True 
        man.left = False
        man.standing = False 
    else:
        # man.right = False 
        # man.left = False 
        man.walkCount = 0
        man.standing = True


    
    if not(man.isJump):
        # if keys[pygame.K_DOWN] and y < 500 - height - vel:
        #     y += vel
        # if keys[pygame.K_UP] and y > vel:
        #     y -= vel
        if keys[pygame.K_UP]:
            man.isJump = True 
            man.right = False 
            man.left = False 
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if(man.jumpCount < 0):
                #we need to fall down
                neg = -1
            #when y is smaller, we jump; when y gets larger, we fall 
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1

        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()
    
    if goblinSpawnTime > 0:
        goblinSpawnTime -= 1
        
    if goblinSpawnTime == 0:
        for i in range(3 - len(goblins)):
            x = randint(20, 300)

            
            # while abs(man.hitbox[1] + man.hitbox[3] - x) < 90 and abs(man.hitbox[1] - x) < 90:
                # x = randint(20, 300)
            

            goblin = enemy(x, 410, 64, 64, 450)
            goblins.append(goblin)
    

  

   
    

  

