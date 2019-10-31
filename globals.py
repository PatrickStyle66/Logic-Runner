from classes import *
W, H = 928, 591

win = pygame.display.set_mode((W, H))

pygame.display.set_caption('Logic Runner!')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()

bgX = 0

bgX2 = bg.get_width()

clock = pygame.time.Clock()

chayenne = pygame.image.load(os.path.join('images','chayenne.jpg'))


server = database('Patrick','','35.198.62.112 ','LogicRunner')

cnx = server.connect()
cursor = cnx.cursor()


pygame.time.set_timer(USEREVENT+1,1000)
pygame.time.set_timer(USEREVENT+2,random.randrange(3000,5000))
speed = 60
run = True

pause = 0
fallSpeed = 0
imunity = 0
undead = 0
objects = []
