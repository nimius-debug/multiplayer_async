import pygame
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../server'))

from network import Network
class GameClient:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Client")
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.player_username = self.get_player_id()
        self.net = Network(self.player_username)
        self.plr = self.net.getP()

    def get_player_id(self):
        player_id = input("Enter your player username: ")
        return player_id

    def redrawWindow(self, players):
        self.win.fill((0, 255, 255))
        for player in players:
            player.draw(self.win)
        pygame.display.update()

    def run(self):
        run = True
        while run:
            dt = self.clock.tick() / 1000
            other_players = self.net.send(self.plr)
            # print(other_players)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            self.plr.update(dt, other_players)
            if other_players is None:
                other_players = []
            self.redrawWindow([self.plr] + other_players)
if __name__ == "__main__":
    client = GameClient()
    client.run()