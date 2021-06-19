import pygame
import random
import time

# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
게임화면크기 = [400, 900]
게임화면 = pygame.display.set_mode(게임화면크기)

게임제목 = "외계인과 전투"
pygame.display.set_caption(게임제목)

# 3. 게임 내 필요한 설정
게임시간 = pygame.time.Clock()


class obj:
    def __init__(입력값):
        입력값.x = 0
        입력값.y = 0
        입력값.move = 0

    def put_img(입력값, address):
        if address[-3:] == "png":
            입력값.img = pygame.image.load(address).convert_alpha()
        else:
            입력값.img = pygame.image.load(address)
            입력값.sx, 입력값.sy = 입력값.img.get_size()

    def change_size(입력값, sx, sy):
        입력값.img = pygame.transform.scale(입력값.img, (sx, sy))
        입력값.sx, 입력값.sy = 입력값.img.get_size()

    def show(입력값):
        게임화면.blit(입력값.img, (입력값.x, 입력값.y))


def 충돌하면(입력값A, 입렵값b):
    if (입력값A.x - 입렵값b.sx <= 입렵값b.x) and (입렵값b.x <= 입력값A.x + 입력값A.sx):
        if (입력값A.y - 입렵값b.sy <= 입렵값b.y) and (입렵값b.y <= 입력값A.y + 입력값A.sy):
            return True
        else:
            return False
    else:
        return False


# 전투기 만들기
전투기 = obj()
전투기.put_img("./image/airplane.png")
전투기.change_size(70, 120)
전투기.x = round(게임화면크기[0] / 2 - 전투기.sx / 2)
전투기.y = 게임화면크기[1] - 전투기.sy - 15
전투기.move = 5
#################################################

왼쪽이동 = False
오른쪽이동 = False
스페이스바 = False

총알목록 = []
외계인목록 = []

검정색 = (0, 0, 0)
흰색 = (255, 255, 255)
증가값 = 0

# 4. 메인 이벤트
멈춤 = 0
while 멈춤 == 0:

    # 4-1. FPS 설정
    게임시간.tick(120)

    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            멈춤 = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                왼쪽이동 = True
            elif event.key == pygame.K_RIGHT:
                오른쪽이동 = True
            elif event.key == pygame.K_SPACE:
                스페이스바 = True
                증가값 = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                왼쪽이동 = False
            elif event.key == pygame.K_RIGHT:
                오른쪽이동 = False
            elif event.key == pygame.K_SPACE:
                스페이스바 = False

    # 4-3. 입력 시간에 따른 변화
    if 왼쪽이동 == True:
        전투기.x -= 전투기.move
        if 전투기.x <= 0:
            전투기.x = 0
    elif 오른쪽이동 == True:
        전투기.x += 전투기.move
        if 전투기.x >= 게임화면크기[0] - 전투기.sx:
            전투기.x = 게임화면크기[0] - 전투기.sx

    if 스페이스바 == True and 증가값 % 6 == 0:
        # 총알 만들기
        총알 = obj()
        총알.put_img("./image/bullet.png")
        총알.change_size(10, 30)
        총알.x = round(전투기.x + 전투기.sx / 2 - 총알.sx / 2)
        총알.y = 전투기.y - 총알.sy - 10
        총알.move = 15
        총알목록.append(총알)
        ###############################################################

    증가값 += 1
    제거목록 = []
    for i in range(len(총알목록)):
        총알수 = 총알목록[i]
        총알수.y -= 총알수.move
        if 총알수.y <= -총알수.sy:
            제거목록.append(i)
    for d in 제거목록:
        del 총알목록[d]

    if random.random() > 0.98:
        # 외계인 만들기
        외계인 = obj()
        외계인.put_img("./image/alien.png")
        외계인.change_size(80, 80)
        외계인.x = random.randrange(0, 게임화면크기[0] - 외계인.sx - round(전투기.sx / 2))
        외계인.y = 10
        외계인.move = 1
        외계인목록.append(외계인)
        ###############################################################

    제거목록 = []
    for i in range(len(외계인목록)):
        외계인수 = 외계인목록[i]
        외계인수.y += 외계인수.move
        if 외계인수.y >= 게임화면크기[1]:
            제거목록.append(i)
    for d in 제거목록:
        del 외계인목록[d]

    제거된총알목록 = []
    제거된외계인목록 = []
    for i in range(len(총알목록)):
        for j in range(len(외계인목록)):
            총알b = 총알목록[i]
            외계인a = 외계인목록[j]
            if 충돌하면(총알b, 외계인a) == True:
                제거된총알목록.append(i)
                제거된외계인목록.append(j)
    제거된총알목록 = list(set(제거된총알목록))
    제거된외계인목록 = list(set(제거된외계인목록))

    for 총알제거 in 제거된총알목록:
        del 총알목록[총알제거]
    for 외계인제거 in 제거된외계인목록:
        del 외계인목록[외계인제거]

    for i in range(len(외계인목록)):
        외계인한명 = 외계인목록[i]
        if 충돌하면(외계인한명, 전투기) == True:
            멈춤 = 1
            time.sleep(1)

    # 4-4. 그리기
    게임화면.fill(검정색)
    전투기.show()
    for 총알하나 in 총알목록:
        총알하나.show()
    for 외계인하나 in 외계인목록:
        외계인하나.show()
    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit