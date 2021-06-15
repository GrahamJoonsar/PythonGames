import pygame, random, time

# Window Setup
windowWidth = 750
windowHeight = 500
pygame.init()
win = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Flappy Bird!")
resetting = False

font = pygame.font.SysFont("Calibri (Body)", 50)

losingText = font.render("You lost", True, (50, 50, 50))
losingTextRect = losingText.get_rect()

losingTextRect.center = (windowWidth // 2, (windowHeight // 2) - 100)

scoreText = font.render("0", True, (50, 50, 50))
scoreTextRect = scoreText.get_rect()

scoreTextRect.center = (25, 25)

class Player:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.yVel = 0.1
        self.dead = False
        self.score = 0

    def update(self):
        # Movement
        if not resetting:
            if self.radius < self.y + self.yVel < windowHeight - self.radius: 
                self.y += self.yVel
            else:
                self.yVel = 0
            self.yVel += 0.2
        # Drawing
        if not self.dead:
            pygame.draw.circle(win, (255, 175, 0), (int(self.x), int(self.y)), self.radius)
        else:
            pygame.draw.circle(win, (0, 0, 0), (int(self.x), int(self.y)), self.radius)

player = Player(150, 250, 20, (255, 175, 0))

class Pipe:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    def move(self):
        if not resetting:
            self.x -= 1


pipePairs = []

def resetPipes():
    for pipe in pipePairs:
        if pipe[0].x < -pipe[0].width:
            pipe[0].x = pipe[1].x = windowWidth
            pipe[0].height = random.randint(30, 350)
            pipe[1].y = pipe[0].height + 125
            pipe[1].height = windowHeight - (pipe[0].height + 125)

def pipeCollision():
    for pipe in pipePairs:
        if 110 < pipe[0].x < 170:
            if player.y < pipe[0].height + 20 or player.y > pipe[1].y - 20:
                player.dead = True


def genPipes():
    pipePairs.clear()
    for i in range(5):
        newPipeTop = Pipe((i + 1) * 150 + 150, 0, 20, random.randint(30, 350), (0, 255, 123))
        newPipeBottom = Pipe((i + 1) * 150 + 150, newPipeTop.height + 125, 20, windowHeight - (newPipeTop.height + 125), (0, 255, 123))
        pipePairs.append([newPipeTop, newPipeBottom])

genPipes()

running = True
timeTilReset = 2000
while running:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.yVel = -4.5
            elif event.key == pygame.K_q:
                running = False
        elif event.type == pygame.QUIT:
            running = False

    win.fill((103, 146, 160))

    player.update()
    
    for pipe in pipePairs:
        pipe[0].draw()
        pipe[0].move()
        pipe[1].draw()
        pipe[1].move()

        if not player.dead and pipe[0].x + 20 == player.x and not resetting:
            player.score += 1
            scoreText = font.render(str(player.score), True, (0, 0, 0))

    resetPipes()
    pipeCollision()

    if player.dead:
        win.blit(losingText, losingTextRect)
        resetting = True

    if resetting:
        timeTilReset -= 10
        if timeTilReset <= 0:
            timeTilReset = 2000
            player.yVel = 0
            player.y = 250
            player.score = 0
            scoreText = font.render(str(player.score), True, (0, 0, 0))
            resetting = False
            player.dead = False
            genPipes()


    win.blit(scoreText, scoreTextRect)

    pygame.display.update()

pygame.quit()