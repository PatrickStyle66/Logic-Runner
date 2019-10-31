from globals import *

pygame.init()

music = pygame.mixer.music.load('Jumper.mp3')
pygame.mixer.music.play(-1)
runner = player(200,468,64,64,'')
def truncline(text, font, maxwidth):
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    old = None
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


def wrapline(text, font, maxwidth):
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)


def redrawWindow():
    global imunity,undead
    win.blit(bg,(bgX,0))
    win.blit(bg,(bgX2,0))
    runner.draw(win)
    for x in objects:
        x.draw(win)
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Pontuação: ' + str(score),1,(255,255,255))
    imunFont = pygame.font.SysFont('comicsans',19)
    imun = font.render('',1,(255,255,255))
    if imunity > 0 and undead > 0:
        if imunity >=250 and imunity <= 500:
            imun = imunFont.render("imunidade!",1,(158, 255, 158))
        elif imunity >=100 :
            imun = imunFont.render("imunidade!", 1,(255,165,0))
        else:
            imun = imunFont.render("Imunidade!",1,(139,0,0))
    win.blit(text,(700,10))
    win.blit(imun,(runner.x - 5, runner.y - 15))
    pygame.display.update()

def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt','w')
        file.write(str(score))
        file.close()
        return score
    return last

def endScreen():
    global pause, objects,speed, score,imunity
    pause = 0
    objects = []
    speed = 60
    imunity = 0
    tryagain = button((0,255,0), 200,420,250,100,'Reiniciar')
    back = button((0,255,0),500,420,250,100,'Menu')
    run = True
    while run:
        pygame.time.delay(100)
        tryagain.draw(win,(0,0,0))
        back.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tryagain.isOver(pos):
                    run = False
                if back.isOver(pos):
                    menu()
                    run = False
        win.blit(bg,(0,0))
        largeFont = pygame.font.SysFont('comicsans',80)
        deathmsg = largeFont.render('Morreu :(',1,(255,255,255))
        win.blit(deathmsg,(W/2 - deathmsg.get_width()/2, 100))
        previousScore = largeFont.render('Melhor Pontuação: ' +str(updateFile()),1,(255,255,255))
        win.blit(previousScore,(W/2 - previousScore.get_width()/2,200))
        newScore = largeFont.render('Pontuação Final: ' + str(score),1,(255,255,255))
        win.blit(newScore, (W / 2 - newScore.get_width() / 2, 320))
    score = 0
    runner.falling = False

def questionScreen():
    global score, pause, imunity
    imunity  = 500
    pause = 0
    run = True
    ButtonA = button((0,255,0),220,350,250,100,'Alternativa A')
    ButtonB = button((0, 255, 0), 220, 470, 250, 100, 'Alternativa B')
    ButtonC = button((0,255,0),520,350,250,100,'Alternativa C')
    ButtonD = button((0, 255, 0), 520, 470, 250, 100, 'Alternativa D')
    font = pygame.font.SysFont('comicsans',30)
    y = font.get_height()
    index = str(random.randrange(1, 11))
    query = (f"SELECT * FROM questions WHERE indice = {index}")
    cursor.execute(query)
    result = cursor.fetchall()
    for sentence in result:
        text = wrapline(sentence[1],font,928)
        questA = font.render('a)' + sentence[2], 1, (255, 255, 255))
        questB = font.render('b)' + sentence[3], 1, (255, 255, 255))
        questC = font.render('c)' + sentence[4], 1, (255, 255, 255))
        questD = font.render('d)' + sentence[5], 1, (255, 255, 255))
        right = sentence[6]
    blits = []
    buttons = [ButtonA,ButtonB,ButtonC,ButtonD]
    correct = buttons.pop(int(right))
    while run:
        pygame.time.delay(100)
        ButtonA.draw(win,(0,0,0))
        ButtonB.draw(win, (0, 0, 0))
        ButtonC.draw(win,(0,0,0))
        ButtonD.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if correct.isOver(pos):
                    run = False
                for wrong in buttons:
                    if wrong.isOver(pos):
                        endScreen()
                        run = False
        win.blit(bg, (0, 0))
        for line in text:
            quest = font.render(line, 1, (255, 255, 255))
            blits.append(win.blit(quest,(0,y)))
            y += font.get_height()
        win.blit(questA,(0,y + font.get_height()))
        win.blit(questB, (0, y + (2 * font.get_height())) )
        win.blit(questC, (0, y + (3 * font.get_height())))
        win.blit(questD, (0, y + (4 * font.get_height())))
        y = font.get_height()
    runner.falling =False


def creditScreen():
    run = True
    back = button((0,255,0),600,25,250 ,100,'Voltar')
    font = pygame.font.SysFont('comicsans', 30)
    patrick = font.render('-Jonathas Patrick H. de Azevedo | jpha@ic.ufal.br',1,(255,255,255))
    thalyssa = font.render('-Thalyssa de Almeida Monteiro | tam@ic.ufal.br',1,(255,255,255))
    cat = font.render('...e chayenne ^ ^',1,(255,255,255))
    copyright = font.render('©2019 Jonathas Patrick',1,(255,255,255))
    music = font.render('Música: Waterflame - Jumper',1,(255,255,255))
    while run:
        pygame.time.delay(100)
        back.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.isOver(pos):
                    run = False
        win.blit(bg, (0, 0))
        win.blit(patrick, (0, 100))
        win.blit(thalyssa, (0, 250))
        win.blit(cat, (0, 350))
        win.blit(chayenne,(10,380))
        win.blit(copyright,(650,550))
        win.blit(music,(50,550))

def player_choose():
    global runner
    logic_im = pygame.image.load(os.path.join('images','S5.png'))
    dummy_im = pygame.image.load(os.path.join('images','dummyS5.png'))
    pygame.display.update()
    run = True
    logic = button((255,255,255),200,150,150,300,'',5)
    dummy = button((255,255,255),400,150,150,300,'',5)
    baldu = button((255,255,255),600,150,150,300,'placeholder',5,30)
    font = pygame.font.SysFont('comicsans',50)
    runfont = pygame.font.SysFont('comicsans',30)
    choose = font.render('Escolha o personagem',1,(255,255,255))
    default = runfont.render('Runner',1,(255,255,255))
    logictxt = runfont.render('Logic',1,(255,255,255))
    dummytxt = runfont.render('Dummy',1,(255,255,255))
    baldutxt = runfont.render('Baldu',1,(255,255,255))
    while run:
        pygame.time.delay(100)
        logic.draw(win,(0,0,0))
        dummy.draw(win,(0,0,0))
        baldu.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if logic.isOver(pos):
                logic = button((0, 255, 0), 200, 150, 150, 300, '', 5)
                logic.draw(win, (0, 0, 0))
                logic_im = pygame.image.load(os.path.join('images', '4.png'))
                pygame.display.update()
            else:
                logic = button((255, 255, 255), 200, 150, 150, 300, '', 5)
                logic.draw(win, (0, 0, 0))
                logic_im = pygame.image.load(os.path.join('images', 'S5.png'))
                pygame.display.update()

            if dummy.isOver(pos):
                dummy = button((0, 255, 0), 400, 150, 150, 300, '', 5)
                dummy.draw(win, (0, 0, 0))
                dummy_im = pygame.image.load(os.path.join('images', 'dummy4.png'))
                pygame.display.update()
            else:
                dummy = button((255, 255, 255), 400, 150, 150, 300, '', 5)
                dummy.draw(win, (0, 0, 0))
                dummy_im = pygame.image.load(os.path.join('images', 'dummyS5.png'))
                pygame.display.update()

            if baldu.isOver(pos):
                baldu = button((0, 255, 0), 600, 150, 150, 300, 'placeholder', 5,30,(255,255,255))
                baldu.draw(win, (0, 0, 0))
                pygame.display.update()
            else:
                baldu = button((255, 255, 255), 600, 150, 150, 300, 'placeholder', 5,30,(255,255,255))
                logic.draw(win, (0, 0, 0))
                pygame.display.update()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if logic.isOver(pos):
                    run = False
                    runner = player(200, 468, 64, 64, '')
                if dummy.isOver(pos):
                    run = False
                    runner = player(200, 468, 64, 64, 'dummy')
        win.blit(bg,(0,0))
        win.blit(choose,(W / 2 - choose.get_width() / 2, 50))
        win.blit(logic_im,(logic.x + (logic.width / 2 - 55 / 2), logic.y + (logic.height / 2 - 64 / 2)))
        win.blit(dummy_im,(dummy.x + (dummy.width / 2 - 55 / 2), dummy.y + (dummy.height / 2 - 66 / 2)))
        win.blit(default,(logic.x + (logic.width / 2 - default.get_width() / 2),logic.y + 270))
        win.blit(default, (dummy.x + (dummy.width / 2 - default.get_width() / 2), dummy.y + 270))
        win.blit(default, (baldu.x + (baldu.width / 2 - default.get_width() / 2), baldu.y + 270))
        win.blit(logictxt,(logic.x + (logic.width / 2 - default.get_width() / 2),logic.y + 270 - default.get_height()))
        win.blit(dummytxt,(dummy.x + (dummy.width / 2 - default.get_width() / 2), dummy.y + 270 - default.get_height()))
        win.blit(baldutxt,(baldu.x + (baldu.width / 2 - default.get_width() / 2), baldu.y + 270 - default.get_height()))

def menu():
    run = True
    start = button((0,255,0),350,250,250,100,'Jogar')
    credit = button((0,255,0),350,400,250,100,'Créditos')
    font = pygame.font.SysFont('minecrafteralt',100)
    soundfont = pygame.font.SysFont('comicsans',30)
    sound1 = soundfont.render('Som(M):On',1,(255,255,255))
    sound2 = soundfont.render('Som(M):Off',1,(255,255,255))
    title = font.render('Logic Runner',1,(255,255,255))
    state = 1
    while run:
        pygame.time.delay(100)
        start.draw(win,(0,0,0))
        credit.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.isOver(pos):
                    run = False
                    pygame.display.update()
                    player_choose()
                if credit.isOver(pos):
                    creditScreen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            state *= -1
            if state == -1:
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.play(-1)
        if state < 0:
            win.blit(sound2,(25,550))
            pygame.display.update()
        else:
            win.blit(sound1,(25,550))
            pygame.display.update()
        win.blit(bg, (0, 0))
        win.blit(title,(W / 2 - title.get_width() / 2, 50))


menu()



while run:
    score = speed//5 - 12
    if imunity > 0:
        imunity -= 1

    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            questionScreen()
            undead = 1

    for objectt in objects:
        if objectt.collide(runner.hitbox) and imunity == 0:
            runner.falling = True
            if pause == 0:
                fallSpeed = speed
                pause = 1
                imunity = 500
                undead = 0

        objectt.x -= 1.4
        if objectt.x < objectt.width * -1:
            objects.pop(objects.index(objectt))

    bgX -= 1.4
    bgX2 -= 1.4
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == USEREVENT+1:
            speed += 1
        if event.type == USEREVENT + 2:
            r = random.randrange(0,2)
            if r == 0:
                objects.append(saw(910,468,64,64))
            else:
                objects.append(spike(910, 0, 48, 472))


    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if not (runner.jumping):
            runner.jumping = True
    if keys[pygame.K_DOWN]:
        if not(runner.sliding):
            runner.sliding = True
    clock.tick(speed)
    redrawWindow()

cursor.close()
cnx.close()

