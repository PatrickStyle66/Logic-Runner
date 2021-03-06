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
    global user
    if user == '':
        f = open('scores.txt', 'r')
        file = f.readlines()
        last = int(file[0])

        if last < int(score):
            f.close()
            file = open('scores.txt', 'w')
            file.write(str(score))
            file.close()
            return score
        return last
    else:
        query =f"SELECT score from scores where user = '{user}'"
        cursor.execute(query)
        result = cursor.fetchall()
        for num in result:
            last = num[0]
        if last < int(score):
            query = f"UPDATE scores SET score = {score} where user = '{user}'"
            cursor.execute(query)
            cnx.commit()
            return score
        return  last

def endScreen():
    global pause, objects,speed, score,imunity
    pause = 0
    objects = []
    speed = 60
    imunity = 0
    tryagain = text_button((0,255,0), 200,420,250,100,std_button('Reiniciar'))
    back = text_button((0,255,0),500,420,250,100,std_button('Menu'))
    run = True
    while run:
        pygame.time.delay(100)

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
        tryagain.draw(win, (0, 0, 0))
        back.draw(win, (0, 0, 0))
        largeFont = pygame.font.SysFont('comicsans',80)
        birdfont = pygame.font.SysFont('comicsans',35,italic=True)
        deathmsg = largeFont.render('Morreu :(',1,(255,255,255))
        win.blit(deathmsg,(W/2 - deathmsg.get_width()/2, 100 - deathmsg.get_height()))
        bird = birdfont.render('"Use a lógica" - Little Bird, 2019',2,(255,255,255))
        win.blit(bird,(W/2 - bird.get_width()/2,150))
        usr_score = str(updateFile())
        previousScore = largeFont.render('Melhor Pontuação: ' + usr_score,1,(255,255,255))
        win.blit(previousScore,(W/2 - previousScore.get_width()/2,200))
        newScore = largeFont.render('Pontuação Final: ' + str(score),1,(255,255,255))
        win.blit(newScore, (W / 2 - newScore.get_width() / 2, 320))
    score = 0
    runner.falling = False

def questionScreen():
    global score, pause, imunity,user,custom_quest
    cnx.commit()
    imunity  = 500
    pause = 0
    run = True
    ButtonA = text_button((0,255,0),220,350,250,100,std_button('Alternativa A'))
    ButtonB = text_button((0, 255, 0), 220, 470, 250, 100, std_button('Alternativa B'))
    ButtonC = text_button((0,255,0),520,350,250,100,std_button('Alternativa C'))
    ButtonD = text_button((0, 255, 0), 520, 470, 250, 100, std_button('Alternativa D'))
    font = pygame.font.SysFont('comicsans',30)
    y = font.get_height()
    if not custom_quest:
        index = str(random.randrange(1, 11))
        query = server.select('*', 'questions', f'indice = {index}')
        cursor.execute(query)
        result = cursor.fetchall()
        for sentence in result:
            text = wrapline(sentence[1], font, 928)
            questA = font.render('a)' + sentence[2], 1, (255, 255, 255))
            questB = font.render('b)' + sentence[3], 1, (255, 255, 255))
            questC = font.render('c)' + sentence[4], 1, (255, 255, 255))
            questD = font.render('d)' + sentence[5], 1, (255, 255, 255))
            right = sentence[6]
    else:
        query = server.select('count(indice)', 'custom_questions', f"user = '{user}'")
        cursor.execute(query)
        result = cursor.fetchall()
        for num in result:
            index = str(random.randrange(1,int(num[0]) + 1))
            query = server.select('*', 'custom_questions', f"indice = {index} and user ='{user}'")
            cursor.execute(query)
            result = cursor.fetchall()
            for sentence in result:
                text = wrapline(sentence[2], font, 928)
                questA = font.render('a)' + sentence[3], 1, (255, 255, 255))
                questB = font.render('b)' + sentence[4], 1, (255, 255, 255))
                questC = font.render('c)' + sentence[5], 1, (255, 255, 255))
                questD = font.render('d)' + sentence[6], 1, (255, 255, 255))
                right = sentence[7]

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
    back = text_button((0,255,0),700,25,125 ,50,std_button('Voltar'))
    font = pygame.font.SysFont('comicsans', 30)
    prog = font.render('Programação geral:',1,(255,255,255))
    patrick = font.render('-Jonathas Patrick H. de Azevedo | jpha@ic.ufal.br',1,(255,255,255))
    sprite = font.render('Sprites do Logic:',1,(255,255,255))
    thalyssa = font.render('-Thalyssa de Almeida Monteiro | tam@ic.ufal.br',1,(255,255,255))
    ic = pygame.image.load(os.path.join('images','ic.png'))
    ufal = pygame.image.load(os.path.join('images', 'ufal.png'))
    data = font.render('Banco de Dados:',1,(255,255,255))
    google = pygame.image.load(os.path.join('images','google_cloud.png'))
    copyright = font.render('©2019 Jonathas Patrick',1,(255,255,255))
    music = font.render('Música: Waterflame - Jumper',1,(255,255,255))
    while run:
        pygame.time.delay(50)
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
        win.blit(prog,(0,100 - patrick.get_height()))
        win.blit(thalyssa, (0, 250))
        win.blit(sprite,(0,250 - thalyssa.get_height()))
        win.blit(copyright,(650,550))
        win.blit(ic,(650,550 - (6 * copyright.get_height())))
        win.blit(ufal,(775,550 - (6 * copyright.get_height())))
        win.blit(data,(0,300))
        win.blit(google,(50,350))
        win.blit(music,(50,550))


def logicfun(logicup):
    return win.blit(logicup, (W / 2 - logicup.get_width() / 2, 550))
def dummyfun(dummyup):
    return win.blit(dummyup, (W / 2 - dummyup.get_width() / 2, 550))
def baldufun(baldup):
    return win.blit(baldup, (W / 2 - baldup.get_width() / 2, 550))

def player_choose():
    global runner
    logic_im = pygame.image.load(os.path.join('images','S5.png'))
    dummy_im = pygame.image.load(os.path.join('images','dummyS5.png'))
    pygame.display.update()
    run = True
    logic = button((255,255,255),200,150,150,300,std_button('',5))
    dummy = button((255,255,255),400,150,150,300,std_button('',5))
    baldu = text_button((255,255,255),600,150,150,300,std_button('Em Breve',5,30))
    back = text_button((0, 255, 0), 700, 25, 125, 50, std_button('Voltar'))
    font = pygame.font.SysFont('comicsans',50)
    runfont = pygame.font.SysFont('comicsans',30)
    choose = font.render('Escolha o personagem',1,(255,255,255))
    default = runfont.render('Runner',1,(255,255,255))
    logictxt = runfont.render('Logic',1,(255,255,255))
    dummytxt = runfont.render('Dummy',1,(255,255,255))
    baldutxt = runfont.render('Baldu',1,(255,255,255))
    blank = runfont.render('',1,(255,255,255))
    logicup = runfont.render('PowerUp: ainda nsei kkk',1,(255,255,255))
    dummyup = runfont.render('PowerUp: Destrói obstáculos ao serem tocados',1,(255,255,255))
    baldup= runfont.render('PowerUp: Transforma os obstáculos em printf, os tornando insignificantes',1,(255,255,255))
    global power
    power = dummyfun
    param = dummyup
    while run:
        pygame.time.delay(100)
        logic.draw(win,(0,0,0))
        dummy.draw(win,(0,0,0))
        baldu.draw(win,(0,0,0))
        back.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():

            pos = pygame.mouse.get_pos()

            if logic.isOver(pos):
                logic = button((0, 255, 0), 200, 150, 150, 300,std_button( '', 5))
                logic.draw(win, (0, 0, 0))
                logic_im = pygame.image.load(os.path.join('images', '4.png'))
                power = logicfun
                param = logicup
                pygame.display.update()
            else:
                logic = button((255, 255, 255), 200, 150, 150, 300,std_button( '', 5))
                logic.draw(win, (0, 0, 0))
                logic_im = pygame.image.load(os.path.join('images', 'S5.png'))
                win.blit(blank, (W / 2 - blank.get_width() / 2, 550))
                pygame.display.update()

            if dummy.isOver(pos):
                dummy = button((0, 255, 0), 400, 150, 150, 300,std_button( '', 5))
                dummy.draw(win, (0, 0, 0))
                dummy_im = pygame.image.load(os.path.join('images', 'dummy4.png'))
                power = dummyfun
                param = dummyup
                pygame.display.update()
            else:
                dummy = button((255, 255, 255), 400, 150, 150, 300, std_button( '', 5))
                dummy.draw(win, (0, 0, 0))
                dummy_im = pygame.image.load(os.path.join('images', 'dummyS5.png'))

                win.blit(blank, (W / 2 - blank.get_width() / 2, 550))
                pygame.display.update()

            if baldu.isOver(pos):
                baldu = text_button((0, 255, 0), 600, 150, 150, 300, std_button('Em breve', 5,30,(255,255,255)))
                baldu.draw(win, (0, 0, 0))
                power = baldufun
                param = baldup
                pygame.display.update()
            else:
                baldu = text_button((255, 255, 255), 600, 150, 150, 300, std_button('Em breve', 5,30,(255,255,255)))
                baldu.draw(win, (0, 0, 0))

                win.blit(blank, (W / 2 - blank.get_width() / 2, 550))
                pygame.display.update()

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if logic.isOver(pos):
                    run = False
                    runner = player(200, 468, 64, 64, '')
                    return False
                if dummy.isOver(pos):
                    run = False
                    runner = player(200, 468, 64, 64, 'dummy')
                    return False
                if back.isOver(pos):
                    return True
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
        power(param)

def rank_menu():
    db = database('Patrick', '', '35.198.62.112 ', 'LogicRunner')
    cnx = server.connect()
    cursor = cnx.cursor()
    run = True
    font = pygame.font.SysFont('comicsans', 30)
    titlefont = pygame.font.Font('Minecrafter.Alt.ttf', 50)
    title = titlefont.render('RAnking', 1, (255, 255, 255))
    back = text_button((0, 255, 0), 700, 25, 125, 50, std_button('Voltar'))
    background = pygame.image.load(os.path.join('images', 'fundo.png'))
    user_font = pygame.font.SysFont('comicsans', 30)
    blits = []
    height = []
    scores = []
    y = 85
    query = "SELECT * from scores order by score desc"
    cursor.execute(query)
    result = cursor.fetchall()
    for request in result:
        friend = font.render(request[0], 1, (255, 255, 255))
        blits.append(friend)
        score = font.render(str(request[1]),1,(255,255,255))
        scores.append(score)
        height.append(y)
        y += font.get_height() + 10

    while run:
        pygame.time.delay(100)
        win.blit(bg, (0, 0))
        win.blit(background, (325, 75))
        back.draw(win, (0, 0, 0))
        i = 0
        if blits == []:
            friend = font.render('Ninguém jogou ;-;', 1, (255, 255, 255))
            win.blit(friend, (325 + (151 - friend.get_width() / 2), 85))
        else:
            for item in blits:
                win.blit(item, (330, height[i]))
                win.blit(scores[i],(600,height[i]))
                i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if back.isOver(pos):
                    run = False

        win.blit(title, (W / 2 - title.get_width() / 2, 30))
        pygame.display.update()
    cnx.close()
    cursor.close()

def friends_list():
    global user
    db = database('Patrick', '', '35.198.62.112 ', 'LogicRunner')
    cnx = server.connect()
    cursor = cnx.cursor()
    run = True
    font = pygame.font.SysFont('comicsans', 30)
    titlefont = pygame.font.Font('Minecrafter.Alt.ttf',50)
    title = titlefont.render('Amigos',1,(255,255,255))
    back = text_button((0, 255, 0), 700, 25, 125, 50,std_button('Voltar'))
    background = pygame.image.load(os.path.join('images', 'fundo.png'))
    user_font = pygame.font.SysFont('comicsans', 30)
    blits = []
    height = []
    users = []
    decline = []
    notblit = []
    y = 85
    query = db.select('friend', 'friends', f"user = '{user}'")
    cursor.execute(query)
    result = cursor.fetchall()
    for request in result:
        friend = font.render(request[0], 1, (255, 255, 255))
        blits.append(friend)
        users.append(request[0])
        decbutton = text_button((255, 0, 0), 600, y, 20, 20, std_button('X', 0, 30, (255, 255, 255)))
        decline.append(decbutton)
        height.append(y)
        y += font.get_height() + 10

    while run:
        pygame.time.delay(100)
        win.blit(bg, (0, 0))
        win.blit(background, (325, 75))
        back.draw(win, (0, 0, 0))
        i = 0
        if blits == []:
            friend = font.render('Sem Amigos ;-;', 1, (255, 255, 255))
            win.blit(friend, (325 + (151 - friend.get_width() / 2), 85))
        else:
            for item in blits:
                win.blit(item, (330, height[i]))
                if i not in notblit:
                    decline[i].draw(win, (0, 0, 0))
                i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if back.isOver(pos):
                    run = False
                for click in decline:
                    if click.isOver(pos):
                        query = f"delete from friends where user = '{user}'and friend = '{users[decline.index(click)]}'"
                        cursor.execute(query)
                        query = f"delete from friends where user = '{users[decline.index(click)]}'and friend = '{user}'"
                        cursor.execute(query)
                        cnx.commit()
                        blits[decline.index(click)] = font.render('Amigo Removido!', 1, (255, 0, 0))
                        users.pop(decline.index(click))
                        notblit.append(decline.index(click))

        profile = user_font.render('Conectado como: ' + user, 1, (255, 255, 255))
        win.blit(profile, (25, 550))
        win.blit(title,(W / 2 - title.get_width() / 2, 30))
        pygame.display.update()
    cnx.close()
    cursor.close()


def request_list():
    global user
    db = database('Patrick','','35.198.62.112 ','LogicRunner')
    cnx = server.connect()
    cursor = cnx.cursor()
    run = True
    font = pygame.font.SysFont('comicsans',30)
    back = text_button((0, 255, 0), 700, 25, 125, 50, std_button('Voltar'))
    background = pygame.image.load(os.path.join('images', 'fundo.png'))
    user_font = pygame.font.SysFont('comicsans', 30)
    titlefont = pygame.font.SysFont('comicsans',50)
    title = titlefont.render('Solicitações',1,(255,255,255))
    blits = []
    height = []
    users = []
    accept = []
    decline = []
    notblit = []
    y = 85
    query = db.select('request', 'friend_request', f"user = '{user}'")
    cursor.execute(query)
    result = cursor.fetchall()
    for request in result:
        friend = font.render(request[0], 1, (255, 255, 255))
        blits.append(friend)
        users.append(request[0])
        accbutton = text_button((0,255,0),570,y,20,20,std_button('√',0,30,(255,255,255)))
        decbutton = text_button((255,0,0),600,y,20,20,std_button('X',0,30,(255,255,255)))
        accept.append(accbutton)
        decline.append(decbutton)
        height.append(y)
        y += font.get_height() + 10


    while run:
        pygame.time.delay(100)
        win.blit(bg,(0,0))
        win.blit(background,(325,75))
        back.draw(win,(0,0,0))
        i = 0
        if blits == []:
            friend = font.render('Sem solicitações ;-;', 1, (255, 255, 255))
            win.blit(friend,(325 + (151 - friend.get_width() / 2),85))
        else:
            for item in blits:
                win.blit(item, (330, height[i]))
                if i not in notblit:
                    accept[i].draw(win, (0, 0, 0))
                    decline[i].draw(win, (0, 0, 0))
                i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if back.isOver(pos):
                    run = False
                for click in accept:
                    if click.isOver(pos):
                        query =f"insert into friends values('{user}','{users[accept.index(click)]}')"
                        cursor.execute(query)
                        query =f"insert into friends values('{users[accept.index(click)]}','{user}')"
                        cursor.execute(query)
                        query = f"delete from friend_request where user = '{user}' and request = '{users[accept.index(click)]}'"
                        cursor.execute(query)
                        cnx.commit()
                        blits[accept.index(click)] = font.render('Aceito!',1,(0,255,0))
                        users.pop(accept.index(click))
                        notblit.append(accept.index(click))

                for click in decline:
                    if click.isOver(pos):
                        query = f"delete from friend_request where user = '{user}'and request = '{users[decline.index(click)]}'"
                        cursor.execute(query)
                        cnx.commit()
                        blits[decline.index(click)] = font.render('Rejeitado!',1,(255,0,0))
                        users.pop(decline.index(click))
                        notblit.append(decline.index(click))

        profile = user_font.render('Conectado como: ' + user, 1, (255, 255, 255))
        win.blit(profile, (25, 550))
        win.blit(title,(W / 2 - title.get_width() / 2, 30))
        pygame.display.update()
    cnx.close()
    cursor.close()

def friends_menu():
    global user,custom_quest
    run = True
    font = pygame.font.Font('Minecrafter.Alt.ttf', 50)
    back = text_button((0, 255, 0), 700, 25, 125, 50, std_button('Voltar'))
    friendlist = text_button((0,255,0),350,155,250,75,std_button('Lista de Amigos',0,40))
    request = text_button((0,255,0),350,255,250,75,std_button('Solicitações'))
    add = text_button((0, 255, 0), 350, 355, 250, 75, std_button('Adicionar Amigo',0,40))
    custom = text_button((0,255,0),350,455,250,75,std_button('Enviar Questões',0,40))
    title = font.render('Amigos',1,(255,255,255))
    user_font = pygame.font.SysFont('comicsans', 30)
    cust_font = user_font.render('Quest. customizadas:',1,(255,255,255))
    query = server.select('indice','custom_questions',f"user = '{user}'")
    cursor.execute(query)
    result = cursor.fetchall()
    blit = False
    if result != []:
        blit = True
    if custom_quest:
        set = 1
    else:
        set = -1
    while run:
        pygame.time.delay(50)
        back.draw(win,(0,0,0))
        add.draw(win,(0,0,0))
        request.draw(win,(0,0,0))
        friendlist.draw(win,(0,0,0))
        custom.draw(win,(0,0,0))
        if custom_quest and blit:
            cust_button = text_button((0,255,0),830,550,75,30,std_button('Sim',0,30,(255,255,255)))
            cust_button.draw(win,(0,0,0))

        elif blit:
            cust_button = text_button((255, 0, 0), 830, 550, 75, 30, std_button('Não', 0, 30, (255, 255, 255)))
            cust_button.draw(win, (0, 0, 0))

        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.isOver(pos):
                    run = False
                if add.isOver(pos):
                    root = Tk()
                    root.geometry('425x125')
                    addFriend(root,user)
                    root.mainloop()
                if request.isOver(pos):
                    request_list()
                if friendlist.isOver(pos):
                    friends_list()
                if custom.isOver(pos):
                    root = Tk()
                    root.geometry('457x540')
                    submit_question(root, user)
                    root.mainloop()
                if blit:
                    if cust_button.isOver(pos):
                        if set == 1:
                            custom_quest = False
                            set = set * -1
                        else:
                            custom_quest = True
                            set = set * - 1

        profile = user_font.render('Conectado como: ' + user, 1, (255, 255, 255))
        win.blit(bg,(0,0))
        win.blit(title, (W / 2 - title.get_width() / 2, 50))
        win.blit(profile, (25, 550))
        if blit:
            win.blit(cust_font, (600, 550))

def acc_menu():
    global user
    run = True
    font = pygame.font.Font('Minecrafter.Alt.ttf',50)
    user_font = pygame.font.SysFont('comicsans',30)
    acc = font.render('ContA',1,(255,255,255))
    back = text_button((0, 255, 0), 700, 25, 125, 50, std_button('Voltar'))
    sign_up = text_button((0, 255, 0), 0, 0, 250, 75, std_button('Registrar-se'))
    sign_in = text_button((0, 255, 0), 0, 0, 250, 75, std_button('Login'))
    friends = text_button((0, 255, 0), 0, 0, 250, 75, std_button('Amigos'))
    log_out = text_button((0, 255, 0), 0, 0, 250, 75, std_button('Desconectar'))
    delete = text_button((0, 255, 0), 0, 0, 250, 75, std_button('Apagar conta'))

    while run:
        pygame.time.delay(50)
        back.draw(win,(0,0,0))
        if user != '':
            friends = text_button((0, 255, 0), 350, 155, 250, 75,std_button('Amigos'))
            log_out = text_button((0, 255, 0), 350, 255, 250, 75, std_button('Desconectar'))
            delete = text_button((0, 255, 0), 350, 355, 250, 75, std_button('Apagar conta'))
            log_out.draw(win,(0,0,0))
            friends.draw(win,(0,0,0))
            delete.draw(win,(0,0,0))

        else:
            sign_up = text_button((0, 255, 0), 350, 155, 250, 75, std_button('Registrar-se'))
            sign_in = text_button((0, 255, 0), 350, 255, 250, 75, std_button('Login'))
            sign_in.draw(win,(0,0,0))
            sign_up.draw(win, (0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sign_up.isOver(pos) and user == '':
                    root = Tk()
                    root.geometry('425x225')
                    register(root)
                    root.mainloop()
                if sign_in.isOver(pos) and user == '':
                    root = Tk()
                    root.geometry('318x183')
                    application = login(root)
                    root.mainloop()
                    user = application.get_user()
                if back.isOver(pos):
                    run = False
                if log_out.isOver(pos) and user != '':
                    user = ''
                    run = False
                if friends.isOver(pos) and user != '':
                    friends_menu()
                if delete.isOver(pos) and user != '':
                    root = Tk()
                    root.geometry('318x183')
                    application = delete_acc(root,user)
                    root.mainloop()
                    user = application.get_user()
                    if user == '':
                        run = False
        if user == '':
            profile = user_font.render('Não conectado',1,(255,255,255))
        else:
            profile = user_font.render('Conectado como: '+ user,1,(255,255,255))
        win.blit(bg,(0,0))
        win.blit(acc,(W / 2 - acc.get_width() / 2, 50))
        win.blit(profile,(25,550))

def menu():
    global state,user
    run = True
    start = text_button((0,255,0),350,175,250,75,std_button('Jogar'))
    account = text_button((0,255,0),350,275,250,75,std_button('Conta'))
    ranking = text_button((0,255,0),350,375,250,75,std_button('Ranking'))
    credit = text_button((0,255,0),350,475,250,75,std_button('Créditos'))
    font = pygame.font.Font('Minecrafter.Alt.ttf',100)
    soundfont = pygame.font.SysFont('comicsans',30)
    sound1 = soundfont.render('Som(M):On',1,(255,255,255))
    sound2 = soundfont.render('Som(M):Off',1,(255,255,255))
    title = font.render('Logic Runner',1,(255,255,255))
    user_font = pygame.font.SysFont('comicsans', 30)
    while run:
        pygame.time.delay(50)
        start.draw(win,(0,0,0))
        credit.draw(win,(0,0,0))
        account.draw(win,(0,0,0))
        ranking.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.isOver(pos):
                   pygame.display.update()
                   run = player_choose()
                if credit.isOver(pos):
                    creditScreen()
                if account.isOver(pos):
                    acc_menu()
                if ranking.isOver(pos):
                    rank_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            state *= -1
            if state == -1:
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.play(-1)
        if state < 0:
            win.blit(sound2,(775,550))
            pygame.display.update()
        else:
            win.blit(sound1,(775,550))
            pygame.display.update()
        if user == '':
            profile = user_font.render('Não conectado',1,(255,255,255))
        else:
            profile = user_font.render('Conectado como: '+ user,1,(255,255,255))
        win.blit(bg, (0, 0))
        win.blit(profile, (25, 550))
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

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if not (runner.jumping):
            runner.jumping = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if not(runner.sliding):
            runner.sliding = True
    clock.tick(speed)
    redrawWindow()

cursor.close()
cnx.close()

