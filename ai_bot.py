import random
from config import VALID_HANDS

class SmartBot:
    def __init__(self):
        self.history = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
        self.last_player_move = None

    def record_move(self, player_move):
        if self.last_player_move is not None:
            self.history[self.last_player_move].append(player_move)
        self.last_player_move = player_move

    def predict_player_move(self):
        if self.last_player_move is not None and self.history[self.last_player_move]:
            past = self.history[self.last_player_move]
            return max(set(past), key=past.count)
        return random.randint(0, 6)

    def get_move(self, is_batting, is_free_hit):
        prediction = self.predict_player_move()
        if not is_batting:
            if prediction == 5 and not is_free_hit:
                return 6 
            return prediction
        else:
            valid_options = [0, 1, 2, 3, 4, 6]
            if is_free_hit: valid_options.append(5)
            if prediction in valid_options: 
                valid_options.remove(prediction)
            return random.choice(valid_options)

    def get_hand_visual(self, move):
        if move in VALID_HANDS:
            return random.choice(VALID_HANDS[move])
        return []