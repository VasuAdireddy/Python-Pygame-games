import pygame as pg,random

pg.init()
wid = 950
hei = 600
dis = pg.display.set_mode((wid,hei))
pg.display.set_caption("Catch_The_Clown")

FPS = 60
clock =pg.time.Clock()

p_s_lives = 5
c_s_vel = 2
c_acc = .3
score = 0
p_lives = p_s_lives
c_vel = c_s_vel
c_dx = random.choice([-1,1])    #-1 is for left dir and  +1 is for right
c_dy = random.choice([-1,1])    #-1 is for up dir and +1 is for down direction

BLUE = (1,175,209)
YELLOW = (248,231,28)

font = pg.font.Font("font1.ttf",32)
title_text = font.render("Catch The Clown",True,(255,75,43))
title_rect = title_text.get_rect()
title_rect.topleft = (15,25)
score_text =font.render("Score : "+ str(score),True,(127,0,255))
score_rect = score_text.get_rect()
score_rect.topright = (wid-50,10)
lives_text = font.render("Lives : "+ str(p_lives),True,(127,0,255))
lives_rect = lives_text.get_rect()
lives_rect.topright = (wid-50,50)
game_over_text = font.render("GAMEOVER",True,BLUE,(255,75,43))
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (wid//2,hei//2)
continue_text = font.render("press any key to PLAY AGAIN",True,YELLOW,(127,0,255))
continue_rect = continue_text.get_rect()
continue_rect.center = (wid//2,hei//2 +64)

h_sound =pg.mixer.Sound("hit.wav")
m_sound = pg.mixer.Sound("miss.wav")
pg.mixer.music.load("Groovy-electronic-background-music.mp3")

bg_image = pg.image.load("Background.png")
bg_rect = bg_image.get_rect()
bg_rect.topleft = (0,0)
clown_image = pg.image.load("clown.png")
clown_image = pg.transform.scale(clown_image,(90,90))
clown_rect = clown_image.get_rect()
clown_rect.center = (wid//2,hei//2)

pg.mixer.music.play(-1,0.0)

run = True
while run:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False
        
        # if click is made
        if i.type == pg.MOUSEBUTTONDOWN:
            mouse_x = i.pos[0]
            mouse_y = i.pos[1]
            # if clicked on clown
            if clown_rect.collidepoint(mouse_x,mouse_y):
                h_sound.play()
                score += 1
                c_vel += c_acc

                #move clown in new dir
                previous_dx = c_dx
                previous_dy = c_dy
                while(previous_dx == c_dx and previous_dy==c_dy):
                    c_dx = random.choice([-1,1])
                    c_dy = random.choice([-1,1])
            # if we miss clown
            else:
                m_sound.play()
                p_lives -= 1
    
    clown_rect.x += c_dx*c_vel
    clown_rect.y += c_dy*c_vel

    #bounce the clowns off the edges
    if clown_rect.left <= 0 or clown_rect.right >= wid:
        c_dx =  -1*c_dx
    if clown_rect.top <= 0 or clown_rect.bottom >= hei:
        c_dy = -1*c_dy

    score_text = font.render("Score : "+ str(score),True,(127,0,255))
    lives_text = font.render("Lives : "+ str(p_lives),True,(127,0,255))

    if p_lives == 0:
        dis.blit(game_over_text,game_over_rect)
        dis.blit(continue_text,continue_rect)
        pg.display.update()

        pg.mixer.music.stop()
        is_paused = True
        while is_paused:
            for j in pg.event.get():
                if j.type == pg.KEYDOWN:
                    score = 0
                    p_lives = p_s_lives
                    clown_rect.center = (wid//2,hei//2)
                    c_vel = c_s_vel
                    c_dx = random.choice([-1,1])
                    c_dy = random.choice([-1,1])
                    pg.mixer.music.play(-1,0.0)
                    is_paused = False
                if j.type == pg.QUIT:
                    is_paused = False
                    run = False

    dis.blit(bg_image,bg_rect)
    dis.blit(score_text,score_rect)
    dis.blit(title_text,title_rect)
    dis.blit(lives_text,lives_rect)
    dis.blit(clown_image,clown_rect)

    pg.display.update()
    clock.tick(FPS)
pg.quit()
