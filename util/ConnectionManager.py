# import pygame
from spriteGroup import all_sprites
class ConnectionManager:
    def __init__(self):
        self.next_connection_id = 0
    
    def get_new_connection_id(self):
        conn_id = self._next_connection_id
        self._next_connection_id += 1
        return conn_id
    
    def add_player(self, player):
        all_sprites.add(player)
        print("Player added: ", player)
        print("All sprites: ", all_sprites)
        
    def remove_player(self, player):
        all_sprites.remove(player)

    def get_all_players(self):
        return all_sprites

    def get_all_players_except(self, player):
        other_players = all_sprites.copy()
        other_players.remove(player)
        return other_players
    
    def get_player(self, user_tag):
        for player in all_sprites:
            if player.user_tag == user_tag:
                return player
        return None
    
    def draw(self, surface, dt):
        all_sprites.draw(surface)
        all_sprites.update(dt)