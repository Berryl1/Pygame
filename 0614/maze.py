import pygame
import sys
import random
import os

# 미로 파일 목록
maze_files = ['maze1.txt', 'maze2.txt', 'maze3.txt']

# 초기 속도
INITIAL_SPEED = 1
# 전역 속도 변수
current_speed = INITIAL_SPEED

# 화면 설정
WIDTH, HEIGHT = 800, 600  # 화면 크기 조정
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

# 플레이어 시작 위치
START_X = 45
START_Y = 45

# 로그 파일 경로
LOG_FILE_PATH = "log.txt"

# 미로를 읽어오는 함수
def read_maze(file_path):
    with open(file_path, "r") as f:
        maze = []
        for line in f:
            maze.append([int(char) for char in line.strip()])
    return maze

# 화면 그리기 함수
def draw(screen, maze, player_pos, reached_goal, hit_wall_count, elapsed_time=None):
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
        text = font.render("Press any key to restart", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        hit_wall_text = font.render(f"Experiences of encountering difficulties: {hit_wall_count}", True, BLACK)
        screen.blit(hit_wall_text, (20, 20))

        if elapsed_time is not None:
            time_text = font.render(f"Time to escape: {elapsed_time:.2f} seconds", True, BLACK)
            screen.blit(time_text, (20, 60))

    pygame.display.flip()

# 로그 파일에 시간을 기록하는 함수
def log_time(file_path, maze_file, elapsed_time):
    with open(file_path, "a") as log_file:
        log_file.write(f"Maze: {maze_file}, Time: {elapsed_time:.2f} seconds\n")

# 메인 함수
def main():
    global current_speed  # 전역 속도 변수 사용
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Predefined Maze Game")
    clock = pygame.time.Clock()

    # 로그 파일 초기화 (처음 실행 시)
    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, "w") as log_file:
            log_file.write("Maze Escape Times:\n")

    while True:
        # 미로 파일을 랜덤하게 선택
        selected_maze_file = random.choice(maze_files)
        print(f"Selected Maze File: {selected_maze_file}")  # 디버깅용 출력

        maze = read_maze(selected_maze_file)
        player_pos = [START_X, START_Y]

        running = True
        reached_goal = False
        hit_wall_count = 0  # 벽에 부딪힌 횟수 초기화

        start_time = pygame.time.get_ticks()  # 게임 시작 시간 기록

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
                    new_pos = [player_pos[0], player_pos[1] - current_speed]  # 예상 이동 위치 계산
                    if maze[new_pos[1] // CELL_SIZE][new_pos[0] // CELL_SIZE] != 1:  # 벽이 아닌 경우에만 이동
                        player_pos = new_pos
                    else:
                        hit_wall_count += 1  # 벽에 부딪힌 횟수 증가
                if keys[pygame.K_s]:
                    new_pos = [player_pos[0], player_pos[1] + current_speed]
                    if maze[new_pos[1] // CELL_SIZE][new_pos[0] // CELL_SIZE] != 1:
                        player_pos = new_pos
                    else:
                        hit_wall_count += 1
                if keys[pygame.K_a]:
                    new_pos = [player_pos[0] - current_speed, player_pos[1]]
                    if maze[new_pos[1] // CELL_SIZE][new_pos[0] // CELL_SIZE] != 1:
                        player_pos = new_pos
                    else:
                        hit_wall_count += 1
                if keys[pygame.K_d]:
                    new_pos = [player_pos[0] + current_speed, player_pos[1]]
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
                    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 경과 시간 계산
                    log_time(LOG_FILE_PATH, selected_maze_file, elapsed_time)  # 로그 파일에 기록

            draw(screen, maze, player_pos, reached_goal, hit_wall_count, elapsed_time if reached_goal else None)
            clock.tick(FPS)

        # 게임 종료 후 속도 증가
        current_speed += 1

if __name__ == "__main__":
    main()
