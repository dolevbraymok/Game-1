
# coding: utf-8


import pygame
from pygame.locals import *
from random import randint


class Player(pygame.sprite.Sprite):
#base class for player with only movment : state attribute is for deciding which way player can jump(if can)
#state can be static ,walking(left or right)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('player.bmp').convert()
        self.rect=self.image.get_rect()
        self.speed=10
        self.movepos=[0,0]
        self.state='static'
        self.jump=False
        self.score=0
        self.fall=False
        self.jumpheight=100
        self.targetheight=0
        self.lives= 10
########################################################################################################

#movement functions for left right and jump 
#the movment functions dont reset self.movepos attribute because it will be reset to 0 at the main script
    def moveleft(self):
        if not self.jump:
            self.movepos[0] = - (self.speed)
            self.state='left'


        
        
    def moveright(self):
        if not self.jump:
            self.movepos[0] = (self.speed)
            self.state='right'
        
        
##suppose to return each time y +speed untill get to certain height or hit the celling
## then start falling untill hit the floor
##need checking if works well

#a jump count from the moment the player jump till he hitting the floor
    def jumping(self):
        if self.jump==True or self.fall==True:
            return
        self.jump=True
        self.targetheight=self.rect.top - self.jumpheight
        
#update the player position and check if its still in game boundries
    def update(self , zgroup):
        if self.jump:
            if self.rect.top > self.targetheight or pygame.sprite.spritecollide(self , zgroup ,False)==None  :
                
                self.movepos[1]=-15
            else :
                #self.nocuts(zgroup)
                self.jump=False
                self.fall=True
                self.movepos[1]=15
        elif self.fall :
            if pygame.sprite.spritecollideany(self , zgroup ,False)==None  :
                self.movepos[1] =15
                
            else:
                
                self.fall=False
                self.movepos[1]=0
        else:
            self.movepos[1]=0
        
        
        newpos=self.rect.move(self.movepos)
        if (newpos.left>=0 and newpos.left<=600) :
            self.rect=newpos
        elif newpos.left <=0 :
            self.rect.move(0,self.movepos[1])
        elif newpos.left >=600 :
            self.rect.move(0,self.movepos[1])
           
        
    
    def collision(self , zgroup):
        z= pygame.sprite.spritecollideany(self , zgroup ,False)
        sr=self.rect
        if z ==None :
            return
        if sr.bottom <= z.rect.top :
            return
        elif sr.top > z.rect.centery - 15 :
            self.rect.top = z.rect.bottom + 2
            self.jump=False
            self.fall=True
        elif (sr.centery < z.rect.centery  and sr.centery >z.rect.top) or sr.botton < x.rect.centery and sr.bottom >x.rec :
            self.rect.bottom = z.rect.top 
        
            
        
        
            
            
    def falling(self, zgroup):
        if pygame.sprite.spritecollideany(self , zgroup ,False)==None and self.jump==False :
            self.fall=True
            
            
######## will work after collision of the player with a monster
    def death(self):
        self.lives -=1
        if self.lives <0 :
            return -1
        else :
            return f'You have {self.lives} left'
            
                
#
#
#
#
#
#
#
#
#
class Zone(pygame.sprite.Sprite ):
    # every floor/ceilling in the game will be a zon object which the player and his npc enemies
    # attributes : size= 0/1/2 0= biggest size , 2= smallest//////deadly=Boolean a zone which you can stay on or not 
    
    def __init__(self , deadly=False , size=0):
        pygame.sprite.Sprite.__init__(self)
        if not deadly:
            if size ==0:
                self.image = pygame.image.load('zone.bmp').convert()
            if size ==1:
                self.image = pygame.image.load('zone 1.bmp').convert()
            if size ==2:
                self.image = pygame.image.load('zone 2.bmp').convert()
            self.rect=self.image.get_rect()
        else:
            if size ==0:
                self.image = pygame.image.load('deadly zone.bmp').convert()
            if size ==1:
                self.image = pygame.image.load('deadly zone 1 .bmp').convert()
            if size ==2:
                self.image = pygame.image.load('deadly zone 2.bmp').convert()
            self.rect=self.image.get_rect()
            
            
        self.deadly=deadly


        
        
        
        
class Enemy(pygame.sprite.Sprite):
#enemy class has the same attributes as player class except enemies are unable to jump    
#enemy state can be only left or right as he cannot be static the beginning spot is decided by the entered state in makeing
#notice if state is left the enemy will start at the right side as the state attribute is which way the enemy is moving
    def __init__(self , x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy.bmp').convert()
        self.rect=self.image.get_rect()
        
        self.movepos=[0,0]
        self.speed=5
        if x==1:
            self.state='left'
            self.rect.center= (450,50)
        elif x==0:
            self.rect.center=(50,50)
            self.state='right'
        else:
            self.rect.center= (450,50)
            self.state='left'
        self.fall=False
    
    def update(self , zgroup ,dzgroup):
        if self.falling(zgroup)== False or self.falling(dzgroup)==False :
            self.fall=False
        else :
            self.fall=True
        if self.fall :
            self.movepos[1]=self.speed
        else:
            z= pygame.sprite.spritecollideany(self,zgroup , False) , pygame.sprite.spritecollideany(self,dzgroup , False)
            if z[0]!= None and self.rect.bottom > z[0].rect.top + 10   :
                self.rect.bottom=z[0].rect.top
            elif z[1] !=None and self.rect.bottom > z[1].rect.top + 10:
                self.rect.bottom=z[1].rect.top
            self.movepos[1]=0
        if self.state=='right' :
            self.movepos[0]=self.speed
        else :
            self.movepos[0]=-self.speed
        newpos=self.rect.move(self.movepos)
          # self.movepos[1]=50
        if (newpos.left>=0 and newpos.left<=600) :
            self.rect=newpos
        elif newpos.left <=0 :
            self.state='right'
            self.rect.move(self.speed,self.movepos[1])
        elif newpos.left >=600 :
            self.state='left'
            self.rect.move(-self.speed,self.movepos[1])
        if self.rect.top >430:
            if randint(0,2)==0 :
                self.rect.center= 50, 50
            else :
                self.rect.center = 400,50
                
           
    

    def falling(self, zgroup):
            if not pygame.sprite.spritecollideany(self,zgroup , False)==None:
                return False
            else:
                return True


 ##MAIN       
pygame.init()        
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Game 1')
# Fill background
background = pygame.Surface(screen.get_size()).convert()
background.fill((0, 0, 0))
#Fonts 
deathfont = pygame.font.SysFont("monospace", 50)
menufont = pygame.font.SysFont("monospace", 35)
sidestats = pygame.font.SysFont("monospace", 15)
white=255,255,255
red= 255,0,0
green=0,255,0
blue=0,0,255
start=menufont.render('Press Enter to Start' , True ,green)
exit=menufont.render('Press ESC to leave' , True ,red)

leave=False
check=False


while (not check):
    
    screen.blit(background,(0,0))
    screen.blit(start,(125,100))
    screen.blit(exit, (140,250))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key==K_RETURN:
            check=True
            break
        elif event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
            pygame.display.quit()
            check=True
            leave=True
            break
if not leave:    
    player = Player() 
    playersprite=pygame.sprite.RenderPlain(player)
    player.rect.center=300,0

    enemy1=Enemy('left')




    #creating a map
    z1=Zone()
    z2=Zone(False,2)
    z3=Zone(False,2)
    z4=Zone(False,1)
    z5=Zone(False,2)
    z6=Zone(False,2)
    z11=Zone(False,2)

    z7=Zone(True,2)
    z8=Zone(True,1)
    z9=Zone(True,1)
    z10=Zone(True)

    z1.rect.center=(300,460)
    z2.rect.center=(50,380)
    z3.rect.center=(600,380)
    z4.rect.center=(600,280)
    z5.rect.center=(50,280)
    z6.rect.center=(280,240)
    z11.rect.center=(280,340)

    z7.rect.center=(300,460)
    z8.rect.center=(50,50)
    z9.rect.center=(500,50)
    z10.rect.center=(375,500)
    #end of map creation
    enemies = pygame.sprite.RenderPlain(enemy1)
    zgroup = pygame.sprite.RenderPlain(z1, z2,z3,z4,z5,z6, z11)
    dzgroup = pygame.sprite.RenderPlain(z7 , z8, z9)


    screen.blit(background, (0, 0))
    zgroup.draw(screen)
    dzgroup.draw(screen)
    pygame.display.flip()


        # Initialise clock

    enemytime=pygame.time.get_ticks()
    clock = pygame.time.Clock()
        # Event loop
    while 1:
            # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)
        if pygame.time.get_ticks() > enemytime+5000:
            if len(enemies.sprites()) <10 :
                Enemy(randint(0,2)).add(enemies)
            enemytime =pygame.time.get_ticks()
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                pygame.display.quit()
                leave=True

            elif event.type == KEYDOWN:

                if event.key == K_LEFT:
                    player.moveleft()
                if event.key == K_RIGHT:
                    player.moveright()

                if event.key == K_UP:
                    player.jumping()



            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    player.movepos[0]=0 
            #if quit event has been activated break the infinte loop
        if leave:
            break

        player.collision(zgroup)
        player.falling(zgroup)
        player.update(zgroup)
        enemies.update(zgroup , dzgroup)

        screen.blit(background, (0, 0))
        screen.blit(background,player ,player)
        for e in enemies:
            screen.blit(background,e,e)

        playersprite.draw(screen)
        enemies.draw(screen)
        zgroup.draw(screen)
        dzgroup.draw(screen)

        stats_list=[f'lives  x{player.lives}' , f'score : {pygame.time.get_ticks()}' ]
        statsrenderd1=sidestats.render(stats_list[0] , True ,blue)
        statsrenderd2=sidestats.render(stats_list[1] , True ,blue)
        screen.blit(statsrenderd1, (0,50))
        screen.blit(statsrenderd2, (0,60))

        pygame.display.flip()
        died=False
        if pygame.sprite.spritecollideany(player , dzgroup) != None or pygame.sprite.spritecollideany(player , enemies) != None or player.rect.bottom > 500 :
            x=player.death()
            if x== -1:
                print('game over')
                player.kill()
            else:
                enemies.empty()
                print(f'{x}')
                player.rect.center= 300,200
                if player.lives>1:
                    lives=f'you have {player.lives} lives left'
                else: lives=f'last try \n  game will continue in {3-i}'
                for i in range(0,3):
                    revive=f'revive in {3-i}'
                    livesrenderd=deathfont.render(lives , True ,white)
                    reviverenderd=deathfont.render(revive , True ,white)
                    screen.blit(background, (0, 0))
                    screen.blit(livesrenderd, (125,100))
                    screen.blit(reviverenderd, (175,250))
                    pygame.display.flip()
                    pygame.time.wait(1000)
                enemytime=pygame.time.get_ticks()

