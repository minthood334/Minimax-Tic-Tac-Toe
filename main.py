import sys
import pygame
from random import randint
from operator import itemgetter
from pygame.locals import QUIT, Rect, MOUSEBUTTONDOWN
from datetime import datetime
sys.setrecursionlimit(99999999)

pygame.init()
pygame.key.set_repeat(5, 5)
pygame.display.set_caption("Tic-Tac-Toe!!")
SURFACE = pygame.display.set_mode((1600, 900))
FPSCLOCK = pygame.time.Clock()
history = []
try:
    f = open("history.txt", 'r')
    for x in f.readlines():
        if x == '':
            continue
        else:
            history.append(list(x.strip().split()))
    f.close()
except:
    f = open("history.txt", 'w')
    f.write('')
    f.close()
print(history)
board = []
check = 0
scroll = 0
def safe(a, b):
    return ( 0 <= a and a <= 3 ) and ( 0 <= a and b <= 3 )

def checkwin(ox):
    return board[0][0] == board[0][1] == board[0][2] == ox or board[1][0] == board[1][1] == board[1][2] == ox or board[2][0] == board[2][1] == board[2][2] == ox or board[0][0] == board[1][0] == board[2][0] == ox or board[0][1] == board[1][1] == board[2][1] == ox or board[0][2] == board[1][2] == board[2][2] == ox or board[0][0] == board[1][1] == board[2][2] == ox or board[0][2] == board[1][1] == board[2][0] == ox

def mini(user, pos):
    global board, opening, check
    alladd = 0
    arr = []
    if not user and checkwin('O'):
        return [0, 0, -1, -1]
    elif user and checkwin('X'):
        return [0, 0, 1, 1]
    elif pos >= 9:
        return [0, 0, 0, 0]
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O' if user else 'X'
                test = mini(not user, pos+1)
                arr.append(list([i, j, test[2], test[3]]))
                if test[3] >= 1:
                    alladd += test[3]
                board[i][j] = ' '
    arr.sort(key=itemgetter(2), reverse = True if not user else False)
    result = arr[0].copy()
    for i in arr:
        if result[2] == i[2] and result[3] < i[3]:
            result = i.copy()
    result[3] = alladd
    return result

def main():
    timer = 0
    mainend = False
    large = pygame.font.SysFont('malgungothic', 56, True).render("TIC TAC TOE", True, (58, 152, 185))
    large_rect = large.get_rect()
    large_rect.center = (800, 350)
    small = pygame.font.SysFont('malgungothic', 24, True).render("COMPUTER VS PLAYER", True, (58, 152, 185))
    small_rect = small.get_rect()
    small_rect.center = (800, 550)
    while not mainend:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if small_rect.collidepoint(event.pos[0], event.pos[1]):
                    mainend = True
                    break
        SURFACE.fill((255, 241, 220))
        SURFACE.blit(large, large_rect)
        rect = Rect(800, 550, 800, 200)
        rect.center = (800, 550)
        pygame.draw.rect(SURFACE, (58, 152, 185), rect, 10)
        if rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            timer += 1
            if timer <= 30:
                rect = Rect(671, 550, 20, 20)
                rect.center = (641, 552.5)
                pygame.draw.rect(SURFACE, (58, 152, 185), rect)
            elif timer <= 60:
                rect = Rect(671, 550, 20, 20)
                rect.center = (641, 552.5)
                pygame.draw.rect(SURFACE, (255, 241, 220), rect)
                if timer >= 60:
                    timer = 0
        else:
            timer = 0
            rect = Rect(671, 550, 20, 20)
            rect.center = (641, 552.5)
            pygame.draw.rect(SURFACE, (58, 152, 185), rect)
        SURFACE.blit(small, small_rect)
        small2 = pygame.font.SysFont('malgungothic', 32, True).render("인하사대부고 20516 이정민", True, (58, 152, 185))
        small2_rect = small2.get_rect()
        small2_rect.center = (800, 800)
        SURFACE.blit(small2, small2_rect)
        FPSCLOCK.tick(60)
        pygame.display.update()
    if mainend:
        InGame()
def InGame():
    global board, check, opening, scroll
    timer = 0
    scroll = 0
    ingameend = False
    gameend = False
    board = [ [ ' ' for j in range(3) ] for i in range(3) ]
    check = 0
    msg = "YOUR TURN"
    scrollbox = Rect(0, 0, 400, 800)
    scrollbox.topleft = (87.5, 50)
    rebox = Rect(0, 0, 350, 75)
    rebox.center = (800, 825)
    bg = Rect(0, 0, 450, 450)
    bg.center = (800, 525)
    retext = pygame.font.SysFont('malgungothic', 32, True).render("다시하기", True, (58, 152, 185))
    retext_rect = retext.get_rect()
    retext_rect.center = (800, 825)
    des = "대전기록은 5개 까지만 저장됩니다."
    print(des)
    destext = pygame.font.SysFont('malgungothic', 20, True).render(des, True, (58, 152, 185))
    destext_rect = destext.get_rect()
    destext_rect.center = (1312.5, 525)
    while not ingameend:   
        now = datetime.now()
        current_time = now.strftime("%Y/%m/%d|%H:%M:%S")
        large = pygame.font.SysFont('malgungothic', 80, True).render(msg, True, (58, 152, 185))
        large_rect = large.get_rect()
        large_rect.center = (800, 150)
        for event in pygame.event.get():
            if event.type == QUIT:
                ingameend = True
            elif not gameend and timer == 0 and event.type == MOUSEBUTTONDOWN and event.button == 1:
                if (event.pos[0] >= 575 and event.pos[0] < 1025) and (event.pos[1] >= 300 and event.pos[1] < 750):
                    xpos = ( event.pos[0] - 575 ) // 150
                    ypos = ( event.pos[1] - 300 ) // 150
                    if board[ypos][xpos] != ' ':
                        continue
                    board[ypos][xpos] = 'O'
                    check += 1
                    if checkwin('O'):
                        msg = 'WIN!!'
                        save(current_time+'|WIN!!')
                        gameend = True
                        continue
                    elif check == 9:
                        msg = 'DRAW'
                        save(current_time+'|DRAW')
                        gameend = True
                        continue
                    timer += 1
                    msg = "AI TURN"
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4 and scrollbox.collidepoint(event.pos[0], event.pos[1]):
                    if scroll > 0:
                        scroll -= 50
                elif event.button == 5 and scrollbox.collidepoint(event.pos[0], event.pos[1]):
                    if 450 + (450 * (len(history) - 1)) >= 800 + scroll + 50:
                        scroll += 50
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if rebox.collidepoint(event.pos[0], event.pos[1]):
                    timer = 0
                    ingameend = False
                    gameend = False
                    board = [ [ ' ' for j in range(3) ] for i in range(3) ]
                    check = 0
                    msg = "YOUR TURN"
        if timer != 0:
            timer += 1
            if timer == 12:
                timer = 0
                res = mini(False, check)
                check += 1
                board[res[0]][res[1]] = 'X'
                msg = "YOUR TURN"
                if checkwin('X'):
                    msg = 'LOSE..'
                    save(current_time+'|LOSE..')
                    gameend = True
        #DRAW
        SURFACE.fill((255, 241, 220))
        pygame.draw.rect(SURFACE, (232, 213, 196), bg)
        mytext = pygame.font.SysFont('malgungothic', 32, True).render("내 모양 : O", True, (58, 152, 185))
        mytext_rect = mytext.get_rect()
        mytext_rect.center = (800, 245)
        SURFACE.blit(mytext, mytext_rect)
        SURFACE.blit(destext, destext_rect)
        for i in range(575, 1175, 150):
            pygame.draw.line(SURFACE, (58, 152, 185), (i, 300), (i, 750), 5)
        for i in range(300, 900, 150):
            pygame.draw.line(SURFACE, (58, 152, 185), (575, i), (1025, i), 5)
        for i in range(3):
            for j in range(3):
                can = pygame.font.SysFont(None, 68).render(board[i][j], True, (58, 152, 185))
                can_rect = can.get_rect()
                can_rect.center = (650 + (150 * j), 375 + (150 * i))
                SURFACE.blit(can, can_rect)
        drawbox()
        pygame.draw.rect(SURFACE, (238, 238, 238), rebox)
        pygame.draw.rect(SURFACE, (58, 152, 185), rebox, 5)
        pygame.draw.rect(SURFACE, (58, 152, 185), scrollbox, 5)
        SURFACE.blit(retext, retext_rect)
        SURFACE.blit(large, large_rect)
        FPSCLOCK.tick(60)
        pygame.display.update()
    main()
def save(a):
    global board
    line = [a]
    for n in board:
        for m in n:
            line.append(m)
    history.append(list(line))
    if len(history) >= 6:
        del history[0]
    f = open("history.txt", 'w')
    msg = ""
    for n in history:
        for m in n:
            msg += m + " "
        msg += "\n"
    f.write(msg)
    f.close()
def drawbox():
    global scroll, history
    for ind in range(len(history)):
        boxrect = Rect(0, 0, 300, 300)
        boxrect.topleft = (137, 150 + (450 * ind) - scroll)
        pygame.draw.rect(SURFACE, (232, 213, 196), boxrect)
        small = pygame.font.SysFont('malgungothic', 24, True).render(history[ind][0], True, (58, 152, 185))
        small_rect = small.get_rect()
        small_rect.center = (287.5, 100 + (450 * ind) - scroll)
        SURFACE.blit(small, small_rect)
        for i in range(len(history[ind]) - 1):
            st = pygame.font.SysFont('malgungothic', 24, True).render(history[ind][i+1], True, (58, 152, 185))
            st_rect = st.get_rect()
            st_rect.center = (187.5 + (100* (i%3)), 200 + (450 * ind) - scroll + (100* (i//3)))
            SURFACE.blit(st, st_rect)
        for i in range(137, 537, 100):
            pygame.draw.line(SURFACE, (58, 152, 185), (i, 150 + (450 * ind) - scroll), (i, 450 + (450 * ind) - scroll), 5)
        for i in range(150 + (450 * ind) - scroll, 550 + (450 * ind) - scroll, 100):
            pygame.draw.line(SURFACE, (58, 152, 185), (137, i), (437, i), 5)
    letterbox = Rect(0, 0, 400, 50)    
    letterbox.topleft = (87.5, 0)
    pygame.draw.rect(SURFACE, (255, 241, 220), letterbox)
    letterbox.bottomleft = (87.5, 900)
    pygame.draw.rect(SURFACE, (255, 241, 220), letterbox)
if __name__ == '__main__':
    main()
