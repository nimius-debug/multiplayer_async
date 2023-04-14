class ConnectionManager:
    def __init__(self):
        self.players = {}
        self._next_connection_id = 0

    def get_new_connection_id(self):
        conn_id = self._next_connection_id
        self._next_connection_id += 1
        return conn_id
    
    def get_all_players(self):
        return self.players
    
    def add_player(self, conn_id, player):
        self.players[conn_id] = player

    def remove_player(self, conn_id):
        if conn_id in self.players:
            del self.players[conn_id]

    def get_player(self, conn_id):
        return self.players.get(conn_id)

    def get_all_players_except(self, conn_id):
        return [player for id, player in self.players.items() if id != conn_id]