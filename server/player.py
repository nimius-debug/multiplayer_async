import pygame

class Player():
    def __init__(self, x, y, width, height, color,user_tag):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3
        self.user_tag = user_tag

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(f"ID: {self.user_tag}", True, (0, 0, 0))
        win.blit(text, (self.x, self.y - 20))
        
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
