import pygame
class Camera:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    # def custom_draw(self, sprites):
    #     ground_offset = self.ground_rect.topleft - self.offset
    #     self.display_surface.blit(self.ground_surf, ground_offset)

    #     for sprite in sorted(sprites, key=lambda sprite: sprite.rect.centery):
    #         offset_pos = sprite.rect.topleft - self.offset
    #         self.display_surface.blit(sprite.image, offset_pos)
