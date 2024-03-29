import pygame
import sys
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Survival Game - Challenge and Overcome")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 플레이어 클래스 정의
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)

    def update(self):
        # 플레이어 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # 화면 경계를 벗어나지 않도록 제한
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

# 장애물 클래스 정의
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((random.randint(20, 50), random.randint(20, 50)))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        # 장애물 아래로 이동
        self.rect.y += self.speedy
        # 화면 밖으로 벗어난 장애물 제거
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# 게임 시작 화면 클래스 정의
class StartScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        text = self.font.render("Press any key to start", True, BLACK)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

# 게임 오버 화면 클래스 정의
class GameOverScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        text = self.font.render("Game Over - Press any key to restart", True, BLACK)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# 장애물 생성
for _ in range(8):
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# 게임 시작 화면
start_screen = StartScreen()

# 게임 오버 화면
game_over_screen = GameOverScreen()

# 게임 루프
running = True
start_game = False
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not start_game:
                start_game = True
            elif game_over:
                # 게임 재시작
                all_sprites.empty()
                obstacles.empty()
                player = Player()
                all_sprites.add(player)
                for _ in range(8):
                    obstacle = Obstacle()
                    all_sprites.add(obstacle)
                    obstacles.add(obstacle)
                game_over = False

    # 게임 시작 전 메인 화면 표시
    if not start_game:
        screen.fill(WHITE)
        start_screen.draw()
        pygame.display.flip()
        continue

    # 게임 오버 여부 확인
    if not game_over:
        # 게임 업데이트
        all_sprites.update()

        # 장애물과 플레이어 충돌 체크
        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            game_over = True

        # 화면을 흰색으로 채우기
        screen.fill(WHITE)

        # 모든 스프라이트 그리기
        all_sprites.draw(screen)

        # 화면 업데이트
        pygame.display.flip()

        # 초당 프레임 설정
        pygame.time.Clock().tick(60)
    else:
        # 게임 오버 화면 표시
        screen.fill(WHITE)
        game_over_screen.draw()
        pygame.display.flip()

