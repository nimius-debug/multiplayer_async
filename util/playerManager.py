import pygame
class PlayerManager:
    def __init__(self):
        self.players = pygame.sprite.Group()   
        
    def add_player(self, player):
        self.players.add(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_all_players(self):
        return self.players

    def get_all_players_except(self, player):
        other_players = self.players.copy()
        other_players.remove(player)
        return other_players
    
    def get_player(self, user_tag):
        for player in self.players:
            if player.user_tag == user_tag:
                return player
        return None
    
    def draw(self, surface):
        self.players.draw(surface)
