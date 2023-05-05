import pygame
from support import *
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, user_tag):
        super().__init__(group)
        self.window = pygame.display.get_surface()
        
        self.load_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        #general setup self.animations[self.status][self.frame_index] 
        self.image = self.animations[self.status][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        # self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 500

        # unique player id
        self.user_tag = user_tag

    def load_assets(self):
        self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}
        
        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
        # print(self.animations)
    
    def animate(self,dt):
        self.frame_index += 4 * dt
        # print(self.frame_index)
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
            
    def detect_collision(self, other_players):
        for other_player in other_players:
               if pygame.sprite.collide_mask(self, other_player) and self.user_tag != other_player.user_tag:
                return True
        return False
    
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def get_status(self):
		# idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

		# tool use
    def move(self, dt, other_players):
        # normalizing a vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        new_pos_x = self.pos.x + self.direction.x * self.speed * dt
        old_rect_x = self.rect.centerx
        self.rect.centerx = new_pos_x
        
        if self.detect_collision(other_players):
            self.rect.centerx = old_rect_x
        else:
            self.pos.x = new_pos_x

        # vertical movement
        new_pos_y = self.pos.y + self.direction.y * self.speed * dt
        old_rect_y = self.rect.centery
        self.rect.centery = new_pos_y
        
        if self.detect_collision(other_players):
            self.rect.centery = old_rect_y
        else:
            self.pos.y = new_pos_y
    
    def update(self, dt, other_players):
        self.input()
        self.get_status()
        
        self.move(dt, other_players)
        self.animate(dt)

    # def draw(self, surface):
    #     for sprite in self.groups()[0]:
    #         sprite.draw(surface)
        
    # def draw(self, surface):
    #     surface.blit(self.image, self.rect)
    #     font = pygame.font.Font(None, 24)
    #     text = font.render(f"ID: {self.user_tag}", True, (0, 0, 0))
    #     surface.blit(text, (self.rect.x + 50 , self.rect.y))
    def draw(self, surface, camera_rect=None):
        if camera_rect is None:
            camera_rect = self.rect
        surface.blit(self.image, camera_rect)
        font = pygame.font.Font(None, 24)
        text = font.render(f"ID: {self.user_tag}", True, (0, 0, 0))
        surface.blit(text, (camera_rect.x + 50 , camera_rect.y))
        
    def draw_with_camera(self, surface, camera):
       
        
        camera_rect = self.rect.move(-camera.offset.x, -camera.offset.y)
        surface.blit(self.image, camera_rect)
        font = pygame.font.Font(None, 24)
        text = font.render(f"ID: {self.user_tag}", True, (0, 0, 0))
        surface.blit(text, (camera_rect.x + 50, camera_rect.y))

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
