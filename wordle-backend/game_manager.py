class GameManager:
    def __init__(self):
        self.games = {}  # 각 방별로 게임 상태를 관리
    
    def create_game(self, room_id, word_list):
        self.games[room_id] = {
            'word_list': word_list,
            'current_word_index': 0,
            'players': [],
            'current_turn': 0
        }

    def add_player(self, room_id, player_id):
        self.games[room_id]['players'].append(player_id)
    
    def get_current_word(self, room_id):
        game = self.games[room_id]
        return game['word_list'][game['current_word_index']]
    
    def next_turn(self, room_id):
        game = self.games[room_id]
        game['current_turn'] = (game['current_turn'] + 1) % len(game['players'])
    
    def check_word(self, room_id, guess):
        current_word = self.get_current_word(room_id)
        return current_word == guess

    def next_word(self, room_id):
        game = self.games[room_id]
        game['current_word_index'] += 1
