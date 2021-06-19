import pygame
import random
import time
from datetime import datetime

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
            충돌효과음()
            return True
        else:
            return False
    else:
        return False


def 충돌효과음():
    pygame.mixer.music.load("./sound/crashAlien.mp3")
    pygame.mixer.music.play(0)


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

게임종료 = 0
외계인죽인횟수 = 0
외계인놓친횟수 = 0

# 4-0. 게임 시작 대기 화면
멈춤 = 0
while 멈춤 == 0:
    게임시간.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                멈춤 = 1
    게임화면.fill(검정색)
    게임화면글꼴 = pygame.font.Font("C:/Windows/Fonts/GULIM.TTC", 20)
    시작텍스트 = 게임화면글꼴.render("스페이스바를 누르면 게임 시작", True, (255, 255, 255))
    게임화면.blit(시작텍스트, (50, round(게임화면크기[1] / 2 - 50)))
    pygame.display.flip()

# 4. 메인 이벤트
시작시간 = datetime.now()
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
    현재시간 = datetime.now()
    시간차 = round((현재시간 - 시작시간).total_seconds())

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
    for i번 in range(len(총알목록)):
        총알수 = 총알목록[i번]
        총알수.y -= 총알수.move
        if 총알수.y <= -총알수.sy:
            제거목록.append(i번)
    제거목록.reverse()
    for d번 in 제거목록:
        del 총알목록[d번]

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
    for i번 in range(len(외계인목록)):
        외계인수 = 외계인목록[i번]
        외계인수.y += 외계인수.move
        if 외계인수.y >= 게임화면크기[1]:
            제거목록.append(i번)
    제거목록.reverse()
    for d번 in 제거목록:
        del 외계인목록[d번]
        외계인놓친횟수 += 1

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

    제거된총알목록.reverse()
    제거된외계인목록.reverse()

    try:
        for 총알제거 in 제거된총알목록:
            del 총알목록[총알제거]
        for 외계인제거 in 제거된외계인목록:
            del 외계인목록[외계인제거]
            외계인죽인횟수 += 1
    except:
        pass

    for i in range(len(외계인목록)):
        외계인한명 = 외계인목록[i]
        if 충돌하면(외계인한명, 전투기) == True:
            멈춤 = 1
            게임종료 = 1

    # 4-4. 그리기
    게임화면.fill(검정색)
    전투기.show()
    for 총알하나 in 총알목록:
        총알하나.show()
    for 외계인하나 in 외계인목록:
        외계인하나.show()

    게임화면글꼴 = pygame.font.Font("C:/Windows/Fonts/GULIM.TTC", 20)
    킬텍스트 = 게임화면글꼴.render(
        "killed : {} loss : {}".format(외계인죽인횟수, 외계인놓친횟수), True, (255, 255, 0)
    )
    게임화면.blit(킬텍스트, (10, 5))

    시간텍스트 = 게임화면글꼴.render("time : {}".format(시간차), True, (255, 255, 255))
    게임화면.blit(시간텍스트, (게임화면크기[0] - 100, 5))
    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
while 게임종료 == 1:
    게임시간.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            게임종료 = 1

    게임화면글꼴 = pygame.font.Font("C:/Windows/Fonts/GULIM.TTC", 40)
    종료텍스트 = 게임화면글꼴.render("게임 종료", True, (255, 0, 0))
    게임화면.blit(종료텍스트, (110, round(게임화면크기[1] / 2 - 50)))
    pygame.display.flip()

pygame.quit