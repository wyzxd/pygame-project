import pygame

pygame.init()
vec = pygame.math.Vector2
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 23
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
JUMP_POWER = 10
GRAVITY = 0.35


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(pygame.Color(0, 0, 0))
        self.rect = pygame.draw.rect(screen, (0, 0, 0), (x, y, WIDTH, HEIGHT))
        self.yvel = 0
        self.onGround = False

    def update(self, left, right, up, platforms):
        if left:
            self.xvel = -MOVE_SPEED
        if right:
            self.xvel = MOVE_SPEED
        if not (left or right):
            self.xvel = 0
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):

                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = pygame.image.load("data/trava.png").convert()
        self.rect = pygame.draw.rect(screen, PLATFORM_COLOR, (x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))


level = [
    "                                          ",
    "                                          ",
    "                                          ",
    "                                          ",
    "                                          ",
    "                                          ",
    "                                          ",
    "                                          ",
    "                                          ",
    "                                          ",
    "       ---                                ",
    "                                          ",
    "    -----------     --            - --    ",
    "                                          ",
    "                    --           -        ",
    "                                          ",
    "                             ----- -   -  ",
    "                       --                 ",
    "       ---   -    ---     ----------      ",
    "                                          ",
    "                                          ",
    "-----------------------------------------"]

hero = Player(33, 700)
entities = pygame.sprite.Group()
platforms = []
entities.add(hero)
left = right = False
up = False
running = True
entities.draw(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            up = True
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            up = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            left = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            right = True
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            right = False
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            left = False
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    entities.draw(screen)
    hero.update(left, right, up, platforms)
    pygame.display.flip()
    screen.fill((66, 170, 255))
    clock.tick(fps)
    print(clock.get_fps())
pygame.quit()
