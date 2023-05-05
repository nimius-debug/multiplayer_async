import pygame
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../server'))
# Add the path of the folder containing the file you want to import
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../util'))
sys.path.insert(0, folder_path)

from Camera import Camera
# from playerManager import PlayerManager
from network import Network
class GameClient:
    def __init__(self):
        
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption("Client")
        pygame.font.init()
        # ground
        self.ground_surf = pygame.image.load('graphics\world\ground.png')
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        self.width = 500
        self.height = 500
        self.win = pygame.display.set_mode((self.width, self.height))
        self.camera = Camera()
        self.clock = pygame.time.Clock()
        self.player_username = self.get_player_id()
        self.net = Network(self.player_username)

        self.plr = self.net.getP()
    
    def get_player_id(self):
        player_id = input("Enter your player username: ")
        return player_id
    
    # def redrawWindow(self, players):
    #     # self.win.fill((0, 255, 255))
    #     self.camera.custom_draw(players)
    #     pygame.display.update()
    def redrawWindow(self, players):
        self.win.fill((0, 255, 255))
        
         # Draw the ground with the camera offset applied
        ground_offset = self.ground_rect.topleft - self.camera.offset
        self.win.blit(self.ground_surf, ground_offset)
        
        for player in players:
            player.draw_with_camera(self.win, self.camera)
        pygame.display.update()

    # def redrawWindow(self, players):
    #     self.win.fill((0, 255, 255))
    #     for player in players:
    #         camera_player = self.camera.apply(player)
    #         player.draw(self.win, camera_player)
    #     pygame.display.update()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def update_players(self, dt):
        other_players = self.net.send(self.plr)
        if other_players is None:
                other_players = []
        self.plr.update(dt, other_players)
        return [self.plr] + other_players
    
    def run(self):
        
        run = True
        while run:
            run = self.handle_events()
            dt = self.clock.tick() / 1000
            players = self.update_players(dt)
            self.camera.center_target_camera(self.plr)
            # self.camera.update(self.plr)
            self.redrawWindow(players)
          
        

if __name__ == "__main__":
    client = GameClient()
    client.run()