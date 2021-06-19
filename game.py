import pygame
import random

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


# 전투기 만들기
Fighter = obj()
Fighter.put_img("./image/airplane.png")
Fighter.change_size(50, 80)
Fighter.x = round(size[0] / 2 - Fighter.sx / 2)
Fighter.y = size[1] - Fighter.sy - 15
Fighter.move = 5
#################################################

left_go = False
right_go = False
space_go = False

bullet_list = []
alien_list = []

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
            elif event.key == pygame.K_SPACE:
                space_go = True
                k = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False

    # 4-3. 입력 시간에 따른 변화
    if left_go == True:
        Fighter.x -= Fighter.move
        if Fighter.x <= 0:
            Fighter.x = 0
    elif right_go == True:
        Fighter.x += Fighter.move
        if Fighter.x >= size[0] - Fighter.sx:
            Fighter.x = size[0] - Fighter.sx

    if space_go == True and k % 6 == 0:
        # 총알 만들기
        bullet = obj()
        bullet.put_img("./image/bullet.png")
        bullet.change_size(5, 15)
        bullet.x = round(Fighter.x + Fighter.sx / 2 - bullet.sx / 2)
        bullet.y = Fighter.y - bullet.sy - 10
        bullet.move = 15
        bullet_list.append(bullet)
        ###############################################################
    k += 1
    delete_list = []
    for i in range(len(bullet_list)):
        b = bullet_list[i]
        b.y -= b.move
        if b.y <= -b.sy:
            delete_list.append(i)
    for d in delete_list:
        del bullet_list[d]

    if random.random() > 0.98:
        # 외계인 만들기
        alien = obj()
        alien.put_img("./image/alien.png")
        alien.change_size(40, 40)
        alien.x = random.randrange(0, size[0] - alien.sx - round(Fighter.sx / 2))
        alien.y = 10
        alien.move = 1
        alien_list.append(alien)
    delete_list = []
    for i in range(len(alien_list)):
        a = alien_list[i]
        a.y += a.move
        if a.y >= size[1]:
            delete_list.append(i)
    for d in delete_list:
        del alien_list[d]
        ###############################################################
    # 4-4. 그리기
    screen.fill(black)
    Fighter.show()
    for b in bullet_list:
        b.show()
    for a in alien_list:
        a.show()
    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit