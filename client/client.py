import pygame
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../server'))
# import os
# import pickle

# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# import Service.connectionManager as conn_mgr
# import Service.player as Player

from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

pygame.init()  # Initialize pygame
pygame.font.init()  # Initialize the font module

def redrawWindow(win, players):
    win.fill((255, 255, 255))
    for player in players:
        player.draw(win)
    pygame.display.update()

def get_player_id():
    player_id = input("Enter your player username: ")
    return player_id

def main():
    run = True
    player_username = get_player_id()
    print('playerusername',player_username)
    net = Network(player_username)
    
    plr = net.getP()
    print("You are", plr)
    clock = pygame.time.Clock()
    
    
    
    while run:
        clock.tick(60)
        other_players = net.send(plr)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        plr.move()
        redrawWindow(win, [plr] + other_players)

if __name__ == "__main__":
    main()
