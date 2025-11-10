import pygame
import sys

# 초기화
pygame.init()
TILE = 100
WIDTH, HEIGHT = 7 * TILE, 7 * TILE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# 맵 정의 (W=벽, .=바닥, G=목표, B=상자, P=플레이어)
level = [
    "WWWWWWW",
    "W....GW",
    "W.B...W",
    "W.P...W",
    "WWWWWWW"
]

# 맵 파싱
player = None
boxes = []
goals = []
walls = []

brick_img = pygame.image.load("./images/brick.png")
brick_img = pygame.transform.scale(brick_img, (TILE, TILE))

player_img = pygame.image.load("./images/player.png")
player_img = pygame.transform.scale(player_img, (TILE, TILE))

box_img = pygame.image.load("./images/box.png")
box_img = pygame.transform.scale(box_img, (TILE, TILE))

goal_img = pygame.image.load("./images/goal.jpg")
goal_img = pygame.transform.scale(goal_img, (TILE, TILE))

for y, row in enumerate(level):
    for x, tile in enumerate(row):
        if tile == "W":
            walls.append((x, y))
        elif tile == "P":
            player = [x, y]
        elif tile == "B":
            boxes.append([x, y])
        elif tile == "G":
            goals.append((x, y))

def draw():
    screen.fill(WHITE)
    # 벽
    for x, y in walls:
        screen.blit(brick_img, (x*TILE, y*TILE))
    # 목표
    for x, y in goals:
        screen.blit(goal_img, (x*TILE, y*TILE))
    # 상자
    for x, y in boxes:
        screen.blit(box_img, (x*TILE, y*TILE))
    # 플레이어
    screen.blit(player_img, (player[0]*TILE, player[1]*TILE))
    pygame.display.update()


def move(dx, dy):
    global player
    new_pos = [player[0]+dx, player[1]+dy]
    if tuple(new_pos) in walls:
        return
    if new_pos in boxes:
        box_new = [new_pos[0]+dx, new_pos[1]+dy]
        if tuple(box_new) in walls or box_new in boxes:
            return
        boxes[boxes.index(new_pos)] = box_new
    player = new_pos

def check_win():
    resunt = all(tuple(b) in goals for b in boxes)
    return resunt

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: move(-1, 0)
            if event.key == pygame.K_RIGHT: move(1, 0)
            if event.key == pygame.K_UP: move(0, -1)
            if event.key == pygame.K_DOWN: move(0, 1)

    draw()
    if check_win():
        print("🎉 클리어!")
        running = False
    clock.tick(30)
