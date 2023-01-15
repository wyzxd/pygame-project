import pygame

pygame.init()
vec = pygame.math.Vector2
size = width, height = 1210, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FFFFFF"
MOVE_SPEED = 3
WIDTH = 22
HEIGHT = 32
JUMP_POWER = 8
GRAVITY = 0.35


def game_over():
    screen.fill((0, 0, 0))
    text = ["Вы прошли игру",
            "Спасибо за то что поиграли в нее."
            ]
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.jump_turn = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image = pygame.transform.scale(pygame.image.load('data/idle/5.png').convert_alpha(), (42, 32))
        self.image_right = pygame.transform.scale(pygame.image.load('data/idle/5.png').convert_alpha(), (42, 32))
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        self.image_jump_right = pygame.transform.scale(pygame.image.load('data/jump/3.png').convert_alpha(), (29, 32))
        self.image_jump_left = pygame.transform.flip(self.image_jump_right, True, False)
        self.image_fall = pygame.transform.scale(pygame.image.load('data/fall/fall.png').convert_alpha(), (42, 32))
        self.rect = pygame.draw.rect(screen, (0, 0, 0), (x, y, WIDTH, HEIGHT))
        self.onGround = False

    def update(self, left, right, up, platforms):
        if left:
            self.image = self.image_left
            self.xvel = -MOVE_SPEED
            self.jump_turn = 1
        if right:
            self.image = self.image_right
            self.xvel = MOVE_SPEED
            self.jump_turn = 0
        if not (left or right):
            self.xvel = 0
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.portal_collide(self.xvel, portals)
        if up:
            if self.jump_turn == 1:
                self.image = self.image_jump_left
            else:
                self.image = self.image_jump_right
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

    def portal_collide(self, xvel, portals):
        for p in portals:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    game_over()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = pygame.image.load('data/trava.png').convert_alpha()
        self.rect = pygame.draw.rect(screen, PLATFORM_COLOR, (x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = pygame.transform.scale(pygame.image.load('data/portal.png').convert_alpha(), (30, 48))
        self.rect = pygame.draw.rect(screen, PLATFORM_COLOR, (x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))


level = [
    "-                                    -",
    "-                                    -",
    "-                                    -",
    "-                                   *-",
    "-                               ------",
    "-                    --  ---         -",
    "-               --                   -",
    "-                                    -",
    "--                                   -",
    "-         ------                     -",
    "-                           ---      -",
    "-                                    -",
    "-                 ------             -",
    "-         ---                        -",
    "-                                    -",
    "-      -----------                   -",
    "-                                    -",
    "-                   -                -",
    "-                      ---  --       -",
    "-                                    -",
    "-                                    -",
    "--------------------------------------"]
camera = Camera()
player = Player(200, 200)
entities = pygame.sprite.Group()
platforms = []
portals = []
entities.add(player)
left = right = False
up = False
running = True
x = y = 0
for row in level:
    for col in row:
        if col == "-":
            pf = Platform(x, y)
            entities.add(pf)
            platforms.append(pf)
        if col == "*":
            pr = Portal(x, y)
            entities.add(pr)
            portals.append(pr)
        x += PLATFORM_WIDTH
    y += PLATFORM_HEIGHT
    x = 0

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
    entities.draw(screen)
    # camera.update(player)
    for sprite in entities:
        camera.apply(sprite)
    player.update(left, right, up, platforms)
    pygame.display.update()
    screen.fill((66, 170, 255))
    clock.tick(fps)
pygame.quit()
