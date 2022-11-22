import pygame as pg,random
pg.init()
wid = 1000
hei = 500
dis = pg.display.set_mode((wid,hei))
pg.display.set_caption("Feed Sagithi")

# Set FPS and Clock
Fps = 60
Clock = pg.time.Clock()

# set game values
Player_starting_lives = 5
Player_vel = 7
cake_start_vel = 5
cake_acc = .25
Buffer_Distance = 100

score = 0
player_Lives = Player_starting_lives
cake_velocity = cake_start_vel

#set colors
green = (0,255,0)
DG = (10,50,10)
White = (255,255,255)
Black = (0,0,0)
yellow = (255,255,0)

#set fonts
font = pg.font.SysFont("calibri",32)
font1 = pg.font.SysFont("Aerial",64)

#set text
score_text = font.render("Score : "+str(score),True,green,DG)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10)

title_text = font1.render("Feed Sagithi", True,yellow,Black)
title_rect =title_text.get_rect()
title_rect.centerx = wid//2

lives_text = font.render("Lives : "+str(player_Lives),True,green,DG)
lives_rect = lives_text.get_rect()
lives_rect.topright = (wid-10,10)

game_over_text = font.render("GAMEOVER",True,green,DG)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (wid//2,hei//2)

continue_text = font.render("Press any key to Play Again", True,green,DG)
continue_rect = continue_text.get_rect()
continue_rect.center = (wid//2,hei//2 + 32)

#set sount and Music
cake_sound = pg.mixer.Sound("sound.wav")
miss_sound = pg.mixer.Sound("sound(lose).wav")
cake_sound.set_volume(.7)
pg.mixer.music.load("sound(Music).wav")

#set images
player_image = pg.image.load("clown.png")
player_image = pg.transform.scale(player_image,(90,90))
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = hei//2

cake_image = pg.image.load("cake.png")
cake_rect = cake_image.get_rect()
cake_rect.x = wid+Buffer_Distance
cake_rect.y = random.randint(64,hei-32)

pg.mixer.music.play(-1,0.0)
run = True
while run:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run =False
    
    keys = pg.key.get_pressed()
    if (keys[pg.K_UP] | keys[pg.K_w]) and player_rect.top >64:
        player_rect.y -= Player_vel
    if (keys[pg.K_DOWN] | keys[pg.K_s]) and player_rect.bottom < hei:
        player_rect.y += Player_vel
    if(keys[pg.K_SPACE]):
        pg.mixer.music.stop()
                
    
    if cake_rect.x<0:
        #plater missed coin
        player_Lives -= 1
        miss_sound.play()
        cake_rect.x = wid+Buffer_Distance
        cake_rect.y = random.randint(64,hei-32)
    else:
        #move coin
        cake_rect.x -= cake_velocity
    
    # check for collision
    if player_rect.colliderect(cake_rect):
        cake_sound.play()
        score += 1
        cake_velocity += cake_acc
        cake_rect.x = wid + Buffer_Distance
        cake_rect.y = random.randint(64,hei-32)
    
    #update the HUD
    score_text = font.render("Score : "+str(score),True,green,DG)
    lives_text = font.render("Lives : "+str(player_Lives),True,green,DG)

    #pause game
    if(keys[pg.K_SPACE]):
        while(1):
            k = pg.key.get_pressed()
            if k[pg.K_SPACE]:
                break
    
    # check for game over
    if player_Lives == 0:
        dis.blit(game_over_text,game_over_rect)
        dis.blit(continue_text,continue_rect)
        pg.display.update()

        #Pause the game until player presses a key, then reset the game
        pg.mixer.music.stop()
        is_paused = True
        while is_paused:
            for i in pg.event.get():
                if i.type == pg.KEYDOWN:
                    score = 0
                    player_Lives = Player_starting_lives
                    player_rect.y = hei//2
                    cake_velocity = cake_start_vel
                    pg.mixer.music.play(-1,0.0)
                    is_paused =False
                #the player wants to quit
                if i.type == pg.QUIT:
                    is_paused = False
                    run = False
    
    dis.fill((0,0,0))
    dis.blit(score_text,score_rect)
    dis.blit(title_text,title_rect)
    dis.blit(lives_text,lives_rect)
    pg.draw.line(dis,White,(0,64),(wid,64),2)
    dis.blit(player_image,player_rect)
    dis.blit(cake_image,cake_rect)

    pg.display.update()
    Clock.tick(Fps)
pg.quit()
