import pygame as py
import time
import random

py.init()

WIDTH = 1000
HEIGHT = 800
WINDOW = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Python Game")
BACK_IMAGE = py.transform.scale(py.image.load("background.jpg"), (WIDTH, HEIGHT))
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 8
FONT = py.font.SysFont("arial", 30)
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 20
PROJECTILE_VEL = 6

def draw(player, elapsed_time, projectiles, score, high_scores):
    WINDOW.blit(BACK_IMAGE, (0, 0))
    time_text = FONT.render(f"Elapsed Time: {round(elapsed_time)}s", 1, "white")
    WINDOW.blit(time_text, (10, 10))
    py.draw.rect(WINDOW, "white", player)
    score_text = FONT.render(f"Score: {int(score)}", 1, "white")
    WINDOW.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    for projectile in projectiles:
        py.draw.rect(WINDOW, "red", projectile)
    py.display.update()


def main():
    run = True
    player  = py.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = py.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    projectile_increment = 2000
    projectile_count = 0
    projectiles = []
    hit = False
    high_scores = [0]

    # Load the previous high score
    try:
        with open("high_score.txt", "r") as file:
            high_scores[0] = float(file.read())
    except FileNotFoundError:
        pass
    
    while run and not hit:
        projectile_count += clock.tick(90)
        elapsed_time = time.time() - start_time
        score = elapsed_time
        if projectile_count > projectile_increment:
            for _ in range(3):
                projectile_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                projectile = py.Rect(projectile_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                projectiles.append(projectile)
            projectile_increment = max(200, projectile_increment - 50)
            projectile_count = 0
            
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                break
        keys = py.key.get_pressed()
        if keys[py.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL 
        if keys[py.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
            
        for projectile in projectiles[:]:
            projectile.y += PROJECTILE_VEL
            if projectile.y > HEIGHT:
                projectiles.remove(projectile)
            elif projectile.y + projectile.height >= player.y and projectile.colliderect(player):
                projectiles.remove(projectile)
                hit = True
                break
            
        if hit:
            lost = FONT.render("You Lost", 1, "white")
            WINDOW.blit(lost, (WIDTH/2 - lost.get_width()/2, HEIGHT/2 - lost.get_height()/2))
            py.display.update()
            py.time.delay(3000)
            break
        
        if score > high_scores[0]:
            high_scores[0] = score

            # Save the new high score
            with open("high_score.txt", "w") as file:
                file.write(str(high_scores[0]))
        
        draw(player, elapsed_time, projectiles, score, high_scores)
        
    high_scores_text = FONT.render(f"Your High Score: {', '.join(map(str, map(int, high_scores)))}", 1, "white")
    WINDOW.blit(high_scores_text, (WIDTH/2 - high_scores_text.get_width()/2, 10))
    py.display.update()
    
    quit_timer = 5000  
    start_quit_time = py.time.get_ticks()

    while py.time.get_ticks() - start_quit_time < quit_timer:
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
        
    py.quit()

if __name__ == "__main__":
    main()