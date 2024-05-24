import pygame
import sys

#speed
SPEED = 1

# 미로 파일의 경로
MAZE_FILE_PATH = "maze.txt"

# 화면 설정
WIDTH, HEIGHT = 800,600  # 화면 크기 조정
FPS = 60

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # 골인 지점 색상

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
START_X = 45
START_Y = 45

# 미로를 읽어오는 함수
def read_maze(file_path):
    with open(file_path, "r") as f:
        maze = []
        for line in f:
            maze.append([int(char) for char in line.strip()])
    return maze

# 화면 그리기 함수
def draw(screen, maze, player_pos, reached_goal, hit_wall_count):
    screen.fill(WHITE)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:  # 벽 그리기
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[y][x] == 0:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[y][x] == 2:  # 골인 지점 그리기
                pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))

    # 골인 지점에 도달하면 메시지 표시
    if reached_goal:
        screen.fill(WHITE)
        font = pygame.font.SysFont(None, 36)
        text = font.render("press any key to restart", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        hit_wall_text = font.render("Experiences of encountering difficulties: {}".format(hit_wall_count), True, BLACK)
        screen.blit(hit_wall_text, (20, 20))

    pygame.display.flip()


# 메인 함수
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Predefined Maze Game")
    clock = pygame.time.Clock()
    set_speed = SPEED

    while True:
        set_speed = set_speed + 1
        maze = read_maze(MAZE_FILE_PATH)
        player_pos = [START_X, START_Y]

        # 속도 설정
        speed = set_speed + 1

        running = True
        reached_goal = False
        hit_wall_count = 0  # 벽에 부딪힌 횟수 초기화
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and reached_goal:
                    running = False

            keys = pygame.key.get_pressed()
            if not reached_goal:
                if keys[pygame.K_w]:
                    new_pos = [player_pos[0], player_pos[1] - speed]  # 예상 이동 위치 계산
                    if maze[new_pos[1] // CELL_SIZE][new_pos[0] // CELL_SIZE] != 1:  # 벽이 아닌 경우에만 이동
                        player_pos = new_pos
                    else:
                        hit_wall_count += 1  # 벽에 부딪힌 횟수 증가
                if keys[pygame.K_s]:
                    new_pos = [player_pos[0], player_pos[1] + speed]
                    if maze[new_pos[1] // CELL_SIZE][new_pos[0] // CELL_SIZE] != 1:
                        player_pos = new_pos
                    else:
                        hit_wall_count += 1
                if keys[pygame.K_a]:
                    new_pos = [player_pos[0] - speed, player_pos[1]]
                    if maze[new_pos[1] // CELL_SIZE][new_pos[0] // CELL_SIZE] != 1:
                        player_pos = new_pos
                    else:
                        hit_wall_count += 1
                if keys[pygame.K_d]:
                    new_pos = [player_pos[0] + speed, player_pos[1]]
                    if maze[new_pos[1] // CELL_SIZE][new_pos[0] // CELL_SIZE] != 1:
                        player_pos = new_pos
                    else:
                        hit_wall_count += 1

                # 경계 체크
                player_pos[0] = max(0, min(WIDTH - PLAYER_SIZE, player_pos[0]))
                player_pos[1] = max(0, min(HEIGHT - PLAYER_SIZE, player_pos[1]))

                # 플레이어가 골인 지점에 도달하면 게임 종료
                if maze[player_pos[1] // CELL_SIZE][player_pos[0] // CELL_SIZE] == 2:
                    reached_goal = True

            draw(screen, maze, player_pos, reached_goal, hit_wall_count)
            clock.tick(FPS)

if __name__ == "__main__":
    main()
