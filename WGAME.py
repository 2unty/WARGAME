import pygame
import array
import time
from pyvidplayer2 import Video
pygame.init()
SW = 960
SH = 540
chax = 0
chay = 0
stridec = 1
transno = 0
foundindx = 0
upperxbound = 150
upperybound = -400
lowerxbound = -150
lowerybound = 15
running = False
wvar = False
avar = False
svar = False
dvar = False
xlock = False
cutscene = True
tick = time.time()
tick1 = time.time()
clock = pygame.time.Clock()
spr = ['BackIdle.png','BackRight.png','BackLeft.png','FrontIdle.png','FrontR.png','FrontL.png','RightIdle.png','RightR.png','RightL.png','LeftIdle.png','LeftR.png','LeftL.png']
imgarray = []
screen = pygame.display.set_mode((SW,SH))
for raw in spr:
	new = pygame.image.load("Sprites/"+raw).convert()
	new.set_colorkey((255,255,255))
	new = pygame.transform.scale(new,(100,100))
	imgarray.append(new)
SWJP = pygame.image.load("Sprites/SWJPSPR.png").convert()
SWJP.set_colorkey((255,255,255))
SWJP = pygame.transform.scale(SWJP,(100,100))
#BI = pygame.image.load('BackIdle.png').convert()
#cha = pygame.Rect((300,250,50,50))
#BI.set_colorkey((255,255,255))
#BI = pygame.transform.scale(BI,(100,100))
SWJPSP = SWJP.get_rect()
SWJPSP.center = (480,-40)
cha = imgarray[0].get_rect()
cha.center = (480,450)
lastspr = imgarray[0]
def interpret(x,y):
	global stridec
	global transno
	global lastspr
	global tick
	global foundindx
	#print(time.time()-tick)
	if time.time()-tick > 0.2:
		stridec+=1
		if stridec > 4:
			stridec = 1
		if stridec == 1 or stridec == 3:
			transno = 0
		elif stridec == 2:
			transno = 1
		elif stridec == 4:
			transno = 2
		tick = time.time()
	
	if y>0:
		foundindx = 3
	elif y<0:
		foundindx = 0
	elif x>0:
		foundindx = 6
	elif x<0:
		foundindx = 9
	else:
		return imgarray[foundindx]
	cha = imgarray[foundindx+transno].get_rect()
	return imgarray[foundindx+transno]
vid = Video("GameIntro.mp4")
vid2 = Video("Straighttoaction.mp4")
vid.resize((960,540))
vid2.resize((960,540))
while cutscene:
	#vid.draw(screen,(0,0))
	#pygame.display.update()
	#print(time.time()-tick1)
	if time.time()-tick1>30:
		vid.close()
		running = True
		cutscene = False
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			vid.close()
			running = True
			cutscene = False
	vid.draw(screen,(0,0),force_draw=False)
	pygame.display.update()
while running:
	screen.fill((84,86,87))
	#pygame.draw.rect(screen,(0,0,255),cha)
	key = pygame.key.get_pressed()
	if key[pygame.K_w] and chay > upperybound and not cutscene: wvar = -1 
	else: wvar = 0
	if key[pygame.K_a] and chax > lowerxbound and not cutscene: avar = -1 
	else: avar = 0
	if key[pygame.K_s] and chay < lowerybound and not cutscene: svar = 1 
	else: svar = 0
	if key[pygame.K_d] and chax < upperxbound and not cutscene: dvar = 1 
	else: dvar = 0
	chax += avar+dvar
	chay += wvar+svar
	#print(chay)
	screen.blit(interpret(avar+dvar,wvar+svar),cha)
	screen.blit(SWJP,SWJPSP)
	tick1=time.time()
	if chay < -325:
		cutscene = True
		while cutscene:
			#vid.draw(screen,(0,0))
			#pygame.display.update()
			if time.time()-tick1>20:
				vid.close()
				running = False
				cutscene = False
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					vid2.close()
					running = False
					cutscene = False
			vid2.draw(screen,(0,0),force_draw=False)
			pygame.display.update()
	if chay > -40:
		cha.move_ip((avar+dvar)*3,(wvar+svar)*3)
	elif chay < -300:
		cha.move_ip((avar+dvar)*3,(wvar+svar)*3)
		SWJPSP.move_ip(0,-(wvar+svar)*3)
	else:
		cha.move_ip((avar+dvar)*3,0)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	pygame.display.update()
	clock.tick(50)
pygame.quit()