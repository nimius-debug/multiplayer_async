import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, user_tag):
        super().__init__(group)

        self.status = 'down'
        self.frame_index = 0

        # general setup
        self.image = pygame.Surface((50, 50))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # unique player id
        self.user_tag = user_tag

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, dt):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.move(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(f"ID: {self.user_tag}", True, (0, 0, 0))
        surface.blit(text, (self.rect.x, self.rect.y - 20))

    def serialize(self):
        return {
            'user_tag': self.user_tag,
            'pos': (self.pos.x, self.pos.y),
            'dir': (self.direction.x, self.direction.y),
        }

    @classmethod
    def deserialize(cls, data):
        pos = data['pos']
        user_tag = data['user_tag']
        group = pygame.sprite.Group()
        player = cls(pos, group, user_tag)
        player.direction = pygame.math.Vector2(data['dir'])
        return player
