import math, pygame

# Window Setup
windowWidth = 1336
windowHeight = 768
pygame.init()
win = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Pygame window!")

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

redTXT = font.render("", False, (90, 90, 90))
blueTXT = font.render("", False, (90, 90, 90))
# Other setup code for your program goes here
def dist(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

MatRadius = 300
bounce = 5
speed = 0.1

debugMode = False
debugLastPressed = False
frozen = False

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y

        self.color = color

        self.xVel = 0
        self.yVel = 0

        self.radius = 40

        self.lost = False
    
    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def update(self, otherPlayer):
        global frozen
        # Moving by velocities
        if not frozen:
            if self.radius < self.x + self.xVel < windowWidth - self.radius:
                self.x += self.xVel
            else:
                self.xVel = 0
            
            if self.radius < self.y + self.yVel < windowHeight - self.radius:
                self.y += self.yVel
            else:
                self.yVel = 0

            # x drag
            if self.xVel >= speed:
                self.xVel -= speed/4
            elif self.xVel <= -speed:
                self.xVel += speed/4
            else:
                self.xVel = 0

            # y drag
            if self.yVel >= speed:
                self.yVel -= speed/4
            elif self.yVel <= -speed:
                self.yVel += speed/4
            else:
                self.yVel = 0
        else:
            a = math.atan2(self.y - otherPlayer.y, self.x - otherPlayer.x)
            pygame.draw.line(win, self.color, (self.x, self.y), (math.cos(a) * bounce * 50 + self.x, math.sin(a) * bounce * 50 + self.y), 4)

        # Collision with other players
        if dist(self.x, self.y, otherPlayer.x, otherPlayer.y) <= self.radius + otherPlayer.radius:
            angle = math.atan2(self.y - otherPlayer.y, self.x - otherPlayer.x)
            self.xVel = math.cos(angle) * bounce
            self.yVel = math.sin(angle) * bounce
            frozen = debugMode

        # Leaving the circle
        lineToCenterColor = (100, 100, 100)
        if dist(self.x, self.y, windowWidth/2, windowHeight/2) > MatRadius:
            lineToCenterColor = (0, 255, 0)
            if not otherPlayer.lost:
                self.lost = True
        if debugMode:
            pygame.draw.line(win, lineToCenterColor, (windowWidth/2, windowHeight/2), (self.x, self.y), 4)


player1 = Player(windowWidth/2 - MatRadius/2, windowHeight/2, (255, 0, 0))
player2 = Player(windowWidth/2 + MatRadius/2, windowHeight/2, (0, 0, 255))

running = True
while running:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # p1
    if keys[pygame.K_w]:
        player1.yVel -= speed
    if keys[pygame.K_s]:
        player1.yVel += speed
    if keys[pygame.K_a]:
        player1.xVel -= speed
    if keys[pygame.K_d]:
        player1.xVel += speed
    
    # p2
    if keys[pygame.K_UP]:
        player2.yVel -= speed
    if keys[pygame.K_DOWN]:
        player2.yVel += speed
    if keys[pygame.K_LEFT]:
        player2.xVel -= speed
    if keys[pygame.K_RIGHT]:
        player2.xVel += speed

    if keys[pygame.K_r]:
        player1 = Player(windowWidth/2 - 150, windowHeight/2, (255, 0, 0))
        player2 = Player(windowWidth/2 + 150, windowHeight/2, (0, 0, 255))
        redTXT = font.render("", False, (90, 90, 90))
        blueTXT = font.render("", False, (90, 90, 90))
    elif keys[pygame.K_p]:
        frozen = False
    elif keys[pygame.K_t]: # Changing to debug mode
        if not debugLastPressed:
            debugMode = not debugMode
        debugLastPressed = True
    else:
        debugLastPressed = False

    win.fill((255, 255, 255))

    pygame.draw.circle(win, (0, 255, 0), (windowWidth/2, windowHeight/2), MatRadius+2)
    pygame.draw.circle(win, (180, 180, 180), (windowWidth/2, windowHeight/2), MatRadius)

    player1.draw()
    player2.draw()

    if debugMode: # drawing line between players
        pygame.draw.line(win, (0, 0, 0), (player1.x, player1.y), (player2.x, player2.y), 4)

    player1.update(player2)
    player2.update(player1)

    if player1.lost:
        redTXT = font.render("Red loses", True, (90, 90, 90))

    if player2.lost:
        blueTXT = font.render("Blue loses", True, (90, 90, 90))

    win.blit(redTXT, (50, 50))
    win.blit(blueTXT, (windowWidth-200, 50))

    pygame.display.update()

pygame.quit()
