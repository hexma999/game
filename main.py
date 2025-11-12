import pygame
import sys
from level import levels

# 초기화
pygame.init()
TILE = 100
WIDTH, HEIGHT = 8 * TILE, 7 * TILE   # level2가 8칸이라 WIDTH 수정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sokoban")

# 색상
WHITE = (255, 255, 255)

# 이미지 로드
brick_img = pygame.transform.scale(pygame.image.load("./images/brick.png"), (TILE, TILE))
player_img = pygame.transform.scale(pygame.image.load("./images/player.png"), (TILE, TILE))
box_img = pygame.transform.scale(pygame.image.load("./images/box.png"), (TILE, TILE))
goal_img = pygame.transform.scale(pygame.image.load("./images/goal.jpg"), (TILE, TILE))

# 맵 초기화 함수
def load_level(level):
    global player, boxes, goals, walls
    player = None
    boxes = []
    goals = []
    walls = []
    
    # 레벨 크기에 맞게 화면 크기 재설정
    WIDTH, HEIGHT = len(level[0]) * TILE, len(level) * TILE
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
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

font = pygame.font.SysFont(None, 50)   # None=기본폰트, 크기=50

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

    # 현재 레벨 표시
    text = font.render(f"Level {current_level+1}", True, (0,0,0))  # 검은색 글자
    screen.blit(text, (10, 10))  # 좌측 상단에 표시

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
    return all(tuple(b) in goals for b in boxes)

# 게임 루프
clock = pygame.time.Clock()
current_level = 0
load_level(levels[current_level])

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
        current_level += 1
        if current_level < len(levels):
            #print("current_level=",current_level,", len=",len(levels))
            load_level(levels[current_level])   # 다음 레벨 불러오기
        else:
            print("모든 레벨 클리어!")
            running = False
    clock.tick(30)