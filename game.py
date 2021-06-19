import pygame

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [400, 900]
screen = pygame.display.set_mode(size)

title = "조상호 게임 만들기"
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()

airplane = pygame.image.load(
    "C:/WebProject/PythonProject/Pygame/airplane.png"
).convert_alpha()
airplane = pygame.transform.scale(airplane, (50, 80))
airplane_sx, airplane_sy = airplane.get_size()
airplane_x = round(size[0] / 2 - airplane_sx / 2)
airplane_y = size[1] - airplane_sy - 15

black = (0, 0, 0)
white = (255, 255, 255)
k = 0

# 4. 메인 이벤트
SB = 0
while SB == 0:

    # 4-1. FPS 설정
    clock.tick(60)

    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1

    # 4-3. 입력 시간에 따른 변화
    k += 1

    # 4-4. 그리기
    screen.fill(black)
    screen.blit(airplane, (airplane_x, airplane_y))

    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit