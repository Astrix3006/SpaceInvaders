import pygame, random, time
from math import sqrt
pygame.init()
pygame.font.init()
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
score = 0 
scores = []
game_window = pygame.display.set_mode((800,600))
font1 = pygame.font.Font("freesansbold.ttf",64)
font2 = pygame.font.Font("freesansbold.ttf",50)
mob = pygame.image.load("enemy.png")
mobX = 1
mobY = 1
go = False
mobY_change = 1
mobX_change = 0
player = pygame.image.load("player.png")
playerX = 450
playerY = 350
enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_count = 6
bullet = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 0
bullet_state = "READY"
sort_once = False
def is_collusion(X1,X2,Y1,Y2,num):
    distance = sqrt(((X2-X1)**2)+((Y2-Y1)**2))
    return distance < num
for i in range(enemy_count):
    enemy.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(50,100))
    enemyY.append(random.randint(1, 740))
    enemyX_change.append(20)
    enemyY_change.append(random.choice([0.5,-0.5]))
running = True
mouse_click1 = (0,0)
show_start_screen = True
show_game_over = False
while running:
    game_window.fill((0,0,0))
    if show_start_screen and not show_game_over:
        game_window.blit((font1.render("SPACE INVADERS",True,(255,255,255))),(100,200))
        pygame.draw.rect(game_window,(0,255,0),((250,350),(250,100)))
        game_window.blit((font2.render("start",True,(0,0,0))),(310,370))
        game_window.blit(mob,(mobY, mobX))
        if mouse_click1[0] >= 260 and mouse_click1[0] <= 510 and mouse_click1[1] >= 350 and mouse_click1[1] <= 450: 
            show_start_screen = False 
        if mobY >= 740:
            mobX_change = 1
            mobY_change = 0
        if mobY <= 0:
            mobX_change = -1
            mobY_change = 0
        if mobX <= 0:
            mobX_change = 0
            mobY_change = 1
            mobX += 1
        if mobX >= 540:
            mobX -= 1
            mobY_change = -1
            mobX_change = 0
        mobY += mobY_change
        mobX += mobX_change
    elif not show_game_over:
        game_window.blit(player,(playerY,playerX))
        playerY = (pygame.mouse.get_pos())[0]
        game_window.blit((font2.render(f"score : {score}",True,(255,255,255))),(310,530))
        if playerY >= 740:
            playerY = 740
        for i in range(enemy_count):
            game_window.blit(enemy[i],(enemyY[i],enemyX[i]))
            if enemyY[i] <= 0:
                enemyY_change[i] *= -1
                enemyX[i] += enemyX_change[i]
            if enemyY[i] >= 740:
                enemyY_change[i] *= -1
                enemyX[i] += enemyX_change[i]
            enemyY[i] += enemyY_change[i]
            if is_collusion(bulletX,enemyX[i],bulletY,enemyY[i],27) and bullet_state == "FIRE":
                bullet_state = "READY"
                enemyX[i] = random.randint(50,100)
                enemyY[i] = random.randint(1, 740)
                if enemyY_change[i] <= 0:
                    enemyY_change[i] += -0.2
                else:
                    enemyY_change[i] += 0.2
                    enemyX_change[i] += 20
                score += 1
            if is_collusion(playerX, enemyX[i],playerY, enemyY[i], 50):
                show_game_over = True
                sort_once = True
        if bullet_state == "FIRE":
            game_window.blit(bullet,(bulletY, bulletX))
            bulletX -= 2
        if bulletX <= 0:
            bullet_state = "READY"
    else:
        if sort_once:
            scores.append(score)
            scores.sort()
            sort_once = False
        pygame.draw.rect(game_window,(0,255,0),((250,230),(260,110)))
        game_window.blit((font2.render(f"Play again",True,(0,0,0))),(250,260))
        game_window.blit((font1.render("Game Over!",True,(255,255,255))),(200,100))
        game_window.blit((font2.render(f"highest score : {scores[-1]}",True,(255,255,255))),(220,400))
        if mouse_click1[1] >= 230 and mouse_click1[1] <= 340 and mouse_click1[0] >= 250 and mouse_click1[0] <= 508:
            show_game_over = False
            for i in range(enemy_count):
                enemyX[i] = random.randint(50,100)
                enemyY[i] = random.randint(1, 740)
                enemyX_change[i] = 20
                enemyY_change[i] = random.choice([0.5,-0.5])
                score = 0
                mouse_click1 = 100,100
                bulletX, bulletX = playerX, playerY
                bullet_state = "READY"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click1 = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state != "FIRE":
                bullet_state = "FIRE"
                bulletX = playerX
                bulletY = playerY
    pygame.display.update()
