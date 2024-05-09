import pygame
import pymunk
import pymunk.pygame_util
import random

def create_ball(space, position, text):
    body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
    body.position = position
    shape = pymunk.Circle(body, 50)
    shape.elasticity = 0.5
    shape.friction = 0.5
    # RGB 색상을 랜덤으로 생성
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    # 색상을 랜덤으로 설정
    shape.color = (r, g, b, 255)  # pymunk에서 색상은 RGBA 형태이므로, A(투명도)는 255로 설정
    
    space.add(body, shape)

    return body, text

def add_floor(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (0, 580), (800, 580), 5)
    shape.elasticity = 0.8
    shape.friction = 1.0
    space.add(body, shape)

def add_walls(space):
    # 왼쪽 벽 생성
    left_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    left_shape = pymunk.Segment(left_body, (0, 0), (0, 600), 5)
    left_shape.elasticity = 0.8
    left_shape.friction = 1.0
    space.add(left_body, left_shape)

    # 오른쪽 벽 생성
    right_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    right_shape = pymunk.Segment(right_body, (800, 0), (800, 600), 5)
    right_shape.elasticity = 0.8
    right_shape.friction = 1.0
    space.add(right_body, right_shape)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 900)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    balls = []
    text_input = ""
    mode = "input"  # 초기 모드를 'input'으로 설정

    add_floor(space)
    add_walls(space)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if mode == "input":  # 텍스트 입력 모드
                    if event.key == pygame.K_RETURN:
                        if text_input:  # 텍스트가 있을 때만 공 생성
                            ball_body, ball_text = create_ball(space, pygame.mouse.get_pos(), text_input)
                            balls.append((ball_body, ball_text))
                            text_input = ""
                            mode = "ball"  # 공 모드로 전환
                        else:
                            mode = "ball"  # 공 모드로 전환하지만 텍스트는 입력하지 않음
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                else:  # 공 모드
                    if event.key == pygame.K_RETURN:
                        mode = "input"  # 텍스트 입력 모드로 전환
            
        screen.fill((255, 255, 255))

        if mode == "ball":  # 공 모드일 때만 공을 그림
            space.debug_draw(draw_options)

            for ball, text in balls:
                font = pygame.font.Font('Maplestory Bold.ttf', 12)
                text_surf = font.render(text, True, (0, 0, 0))
                screen.blit(text_surf, (int(ball.position.x) - 30, int(ball.position.y)))

        if mode == "input":  # 텍스트 입력 모드일 때 입력 중인 텍스트 표시
            font = pygame.font.Font('Maplestory Bold.ttf', 24)
            prompt_text = "텍스트를 입력하세요 : " + text_input
            input_surf = font.render(prompt_text, True, (0, 0, 0))
            screen.blit(input_surf, (150, 250))  # 화면의 상단에 텍스트 입력 표시
        
        space.step(1/50.0)
        pygame.display.flip()
        clock.tick(50)
    
    pygame.quit()

if __name__ == '__main__':
    main()
