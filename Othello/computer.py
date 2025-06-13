import time
from Othello.othello import Othello
from Othello.othello import Player
import copy
class Computer():
    def __init__(self,game):
        self.coin = 0
        self.game = game
        self.MAX_DEPTH = 5
        self.MAX_TIME = 1
        self.hashMapStanja = {}
    #heuristic for the computer player

    def calculate_coin_parity(self, max_player_coins, min_player_coins):
        return 100 * (max_player_coins - min_player_coins) / (max_player_coins + min_player_coins)

    def calculate_mobility(self, max_player_moves, min_player_moves):
        if max_player_moves + min_player_moves != 0:
            return 100 * (max_player_moves - min_player_moves) / (max_player_moves + min_player_moves)
        else:
            return 0

    def calculate_corner(self, max_player_corners, min_player_corners):
        if max_player_corners + min_player_corners != 0:
            return 100 * (max_player_corners - min_player_corners) / (max_player_corners + min_player_corners)
        else:
            return 0

    def calculate_stability(self, max_player_stability, min_player_stability):
        if max_player_stability + min_player_stability != 0:
            return 100 * (max_player_stability - min_player_stability) / (max_player_stability + min_player_stability)
        else:
            return 0
    def is_stable(game_state, row, col):
        if (row == 0 and col == 0) or (row == 0 and col == 7) or (row == 7 and col == 0) or (row == 7 and col == 7):
            return True
        
        return False

    def get_max_player_coins(self, game_state):
        max_player_coins = 0
        for row in range(0,8):
            for col in range(0,8):
                if game_state[row][col] == Player.white.value:
                    max_player_coins+=1
        return max_player_coins
    
    def get_min_player_coins(self, game_state):
        min_player_coins = 0
        for row in range(0,8):
            for col in range(0,8):
                if game_state[row][col] == Player.black.value:
                    min_player_coins+=1
        return min_player_coins
    
    def get_max_player_moves(self, game_state):
        max_player_moves = 0
        moves = self.game.find_legal_moves(Player.white)
        for move in moves:
            self.game.make_move(Player.white,move, moves[move])
            if self.game.find_curr_player() == Player.white:
                max_player_moves+=1

        return max_player_moves
    
    def get_min_player_moves(self, game_state):
        min_player_moves = 0
        moves = self.game.find_legal_moves(Player.black)
        for move in moves:
            self.game.make_move(Player.black,move, moves[move])
            if self.game.find_curr_player() == Player.black:
                min_player_moves+=1

        return min_player_moves
    
    def get_max_player_corners(self, game_state):
        max_player_corners = 0
        if game_state[0][0] == Player.white.value:
            max_player_corners+=1
        if game_state[7][7] == Player.white.value:
            max_player_corners+=1
        if game_state[7][0] == Player.white.value:
            max_player_corners+=1
        if game_state[0][7] == Player.white.value:
            max_player_corners+=1
        return max_player_corners
    
    def get_min_player_corners(self, game_state):
        min_player_corners = 0
        if game_state[0][0] == Player.black.value:
            min_player_corners+=1
        if game_state[7][7] == Player.black.value:
            min_player_corners+=1
        if game_state[7][0] == Player.black.value:
            min_player_corners+=1
        if game_state[0][7] == Player.black.value:
            min_player_corners+=1

        return min_player_corners
        
    def get_max_player_stability(self, game_state):
        max_player_stability = 0

        for row in range(0,8):
            for col in range(0,8):
                if game_state[row][col] == Player.white:  
                    if self.is_stable(game_state, row, col):
                        max_player_stability += 1
        return max_player_stability
    def get_min_player_stability(self, game_state):
        min_player_stability = 0

        for row in range(0,8):
            for col in range(0,8):
                if game_state[row][col] == Player.black:  
                    if self.is_stable(game_state, row, col):
                        min_player_stability += 1
        return min_player_stability
    
    

    #evaluate all the heuristics
    def evaluate(self, game_state):
        game = self.game
        max_player_coins = self.get_max_player_coins(game_state)
        min_player_coins = self.get_min_player_coins(game_state)

        max_player_moves = self.get_max_player_moves(game_state)
        min_player_moves = self.get_min_player_moves(game_state)

        max_player_corners = self.get_max_player_corners(game_state)
        min_player_corners = self.get_min_player_corners(game_state)

        max_player_stability = self.get_max_player_stability(game_state)
        min_player_stability = self.get_min_player_stability(game_state)


        score = self.calculate_coin_parity(max_player_coins, min_player_coins)
        + self.calculate_mobility(max_player_moves, min_player_moves)
        + self.calculate_corner(max_player_corners, min_player_corners)
        + self.calculate_stability(max_player_stability, min_player_stability)

        return score

    def minimax(self, game_state, depth, alpha, beta , maximizng_player, start_time):
        if depth == 0 or self.game.is_game_over():
            return self.evaluate(game_state)
        
        if maximizng_player:
            max_eval = float("-inf")
            moves = self.game.find_legal_moves(Player.white, game_state)
            for move in moves:
                new_state, nista = self.game.make_move(Player.white,move, moves[move], game_state)
                eval = self.minimax(new_state, depth - 1, alpha, beta, False, start_time)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
                if time.time() - start_time >= self.MAX_TIME:
                    return max_eval
            return max_eval
        
        else:
            min_eval = float("inf")
            moves = self.game.find_legal_moves(Player.black, game_state)
            for move in moves:
                new_state, nista = self.game.make_move(Player.black, move, moves[move], game_state)
                eval = self.minimax(new_state, depth-1, alpha, beta, True, start_time)
                min_eval = min(eval, min_eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
                if time.time() - start_time >= self.MAX_TIME:
                    return min_eval
            return min_eval

    def get_best_move(self, game_state):


        start_time = time.time()
        best_move = None
        max_eval = float("-inf")
        game_state_before = copy.deepcopy(game_state)
        self.game.table = game_state
        game_finished = copy.deepcopy(self.game.game_over)


       
        alpha = float("-inf")
        beta = float("inf")

            #skontaj kako da nadjes legalne poteze moras proslijediti dobar self!


        moves = self.game.find_legal_moves(Player.white)
        for move in moves:
                new_state, nista = self.game.make_move( Player.white, move, moves[move])
                eval = self.minimax(new_state, self.MAX_DEPTH, alpha, beta , False, start_time)


                if eval > max_eval:
                    max_eval = eval
                    best_move = move
        self.game.currPlayer = Player.white
        self.game.nextPlayer = Player.black
       
        self.game.game_over = game_finished
        valid, outflanked = self.game.is_move_legal(Player.white, best_move, [], game_state_before)
        if time.time() - start_time >= self.MAX_TIME:
            return best_move, outflanked
        return best_move, outflanked
