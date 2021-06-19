import pygame
from pygame.constants import K_RIGHT

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [400, 900]
screen = pygame.display.set_mode(size)

title = "조상호 게임 만들기"
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()


class obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0

    def put_img(self, address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
            self.sx, self.sy = self.img.get_size()

    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()

    def show(self):
        screen.blit(self.img, (self.x, self.y))


gameClass = obj()
gameClass.put_img("./airplane.png")
gameClass.change_size(50, 80)
gameClass.x = round(size[0] / 2 - gameClass.sx / 2)
gameClass.y = size[1] - gameClass.sy - 15
gameClass.move = 5

left_go = False
right_go = False

black = (0, 0, 0)
white = (255, 255, 255)
k = 0

# 4. 메인 이벤트
STOP = 0
while STOP == 0:

    # 4-1. FPS 설정
    clock.tick(60)

    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            STOP = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_go = True
            elif event.key == pygame.K_RIGHT:
                right_go = True
        elif event.type = pygame.KEYUP:
          if event.key == pygame.K_LEFT:
              left_go = False
          elif event.key == pygame.K_RIGHT:
              right_go = False

    # 4-3. 입력 시간에 따른 변화

    # 4-4. 그리기
    screen.fill(black)
    gameClass.show()

    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quitV