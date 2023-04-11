import pygame
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
    net = Network(player_username)
    p = net.getP()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        other_players = net.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, [p] + other_players)

main()
