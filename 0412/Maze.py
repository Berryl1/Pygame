import pygame
import sys

# 미로 파일의 경로
MAZE_FILE_PATH = "maze.txt"

# 화면 설정
WIDTH, HEIGHT = 800, 600
FPS = 30

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 셀 크기
CELL_SIZE = 40

# 플레이어 설정
PLAYER_SIZE = 20  # 크기 조정

# 방향
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# 플레이어 시작 위치
START_X = 30
START_Y = 30

# 미로를 읽어오는 함수
def read_maze(file_path):
    with open(file_path, "r") as f:
        maze = []
        for line in f:
            maze.append([int(char) for char in line.strip()])
    return maze

# 화면 그리기 함수
def draw(screen, maze, player_pos):
    screen.fill(WHITE)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))
    pygame.display.flip()

# 속도 설정 함수
def set_speed():
    speed = input("Please write down your pace of life (1-100): ")
    while not speed.isdigit() or int(speed) < 1 or int(speed) > 100:
        speed = input("Invalid input. Please enter a number between 1 and 100: ")
    return int(speed)

# 메인 함수
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Predefined Maze Game")
    clock = pygame.time.Clock()

    maze = read_maze(MAZE_FILE_PATH)
    player_pos = [START_X, START_Y]

    # 속도 설정
    speed = set_speed()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos[1] -= speed  # 속도 적용
        if keys[pygame.K_s]:
            player_pos[1] += speed  # 속도 적용
        if keys[pygame.K_a]:
            player_pos[0] -= speed  # 속도 적용
        if keys[pygame.K_d]:
            player_pos[0] += speed  # 속도 적용

        # 경계 체크
        player_pos[0] = max(0, min(WIDTH - PLAYER_SIZE, player_pos[0]))
        player_pos[1] = max(0, min(HEIGHT - PLAYER_SIZE, player_pos[1]))

        draw(screen, maze, player_pos)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
