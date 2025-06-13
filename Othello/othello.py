import copy
from enum import Enum

class Player(Enum):
    black = 1
    white = -1
    empty = None

class Othello():
    def __init__(self):
        self.table = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, -1, 0, 0, 0],
            [0, 0, 0, -1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.currPlayer = Player.black
        self.nextPlayer = Player.white
        self.outflanked = {}
        self.disc_count = {
            Player.black: 2,
            Player.white: 2
        }
        self.game_over = False
    def change_player(self):
        if self.currPlayer == Player.white:
            self.currPlayer = Player.black
            self.nextPlayer = Player.white
            
        elif self.currPlayer == Player.black:
            self.currPlayer = Player.white
            self.nextPlayer = Player.black

        else:
            self.nextPlayer = Player.empty

    def is_inside_board(self, row, column):
        if row < 0 or row > 7 or column < 0 or column > 7:
            return False
        return True

    def outflanked_in_dir(self, position, player, rDelta, cDelta):
        outflanked = []
        r = position[0] + rDelta
        c = position[1] + cDelta

        while self.is_inside_board(r, c) and self.table[r][c] != 0:
            val = self.nextPlayer.value
            if self.table[r][c] == self.nextPlayer.value:
                outflanked.append((r, c))
                r += rDelta
                c += cDelta
            else:  # self.table[r][c] == player.value[0]:
                return outflanked
        return []

    def in_all_dir(self, position, player):
        outflanked = []
        for rDelta in range(-1, 2):
            for cDelta in range(-1, 2):
                if rDelta == 0 and cDelta == 0:
                    continue
                outflanked.extend(self.outflanked_in_dir(position, player, rDelta, cDelta))
        return outflanked

    def is_move_legal(self, player, position, outflanked, board = None):
        if board != None:
            self.table = board
        if position is None or self.table[position[0]][position[1]] != 0:
            outflanked = None
            return False, outflanked
        outflanked = self.in_all_dir(position, player)
        length = len(outflanked)
        return [length > 0, outflanked]
    

    def find_legal_moves(self, player, board = None):
        moves = {}
        for i in range(8):
            for j in range(8):
                pos = (i, j)
                [legal, outflankeded] = self.is_move_legal(player, pos, self.outflanked, board)
                if legal:
                    moves[pos] = outflankeded
        return moves

    def play_game(self):
        ROWS = 8
        COLS = 8
        game_over = False
        
        winner = Player.empty
        possible_moves = {
            (0, 0): []
        }

        legal_moves = self.find_legal_moves(self.currPlayer)
        for i in legal_moves:
            possible_moves[i] = legal_moves[i]

        if self.currPlayer == Player.white:
            print("White Turn:")
        elif self.currPlayer == Player.black:
            print("Black Turn:")

    def update_disc_count(self, currPlayer ,outflanked, nextPlayer):
        if currPlayer != Player.empty and nextPlayer != Player.empty:
            self.disc_count[currPlayer] += len(outflanked) + 1
            self.disc_count[nextPlayer] -= len(outflanked)

    def find_winner(self):
        if self.disc_count[Player.black] > self.disc_count[Player.white]:
            return Player.black
        elif self.disc_count[Player.black] < self.disc_count[Player.white]:
            return Player.white
        else:
            return Player.empty
    def pass_turn(self, nova_tabla = None):
        self.change_player()
        if nova_tabla != None:
            self.table = nova_tabla
        if self.find_legal_moves(self.currPlayer) != {}:
            return
        self.change_player()
        if self.find_legal_moves(self.currPlayer) == {}:
            self.currPlayer = Player.empty
            self.game_over = True
            self.find_winner()
    

    def is_table_full(self):
        for i in range(8):
            for j in range(8):
                if self.table[i][j] == 0:
                    return False
        return True
    def is_game_over(self):
        return self.game_over
    def find_curr_player(self):
        return self.currPlayer

    def make_move(self,currentPlayer ,position, outflanked, game_state = None):
        if game_state != None:
            nova_tabla = copy.deepcopy(game_state)
        else:
            nova_tabla = copy.deepcopy(self.table)
        nova_tabla[position[0]][position[1]] = currentPlayer.value


        for i in outflanked:
            nova_tabla[i[0]][i[1]] = currentPlayer.value

        self.update_disc_count(self.currPlayer, outflanked, self.nextPlayer)
        
        self.pass_turn()
        

        return nova_tabla, self.game_over
    
        #update disc count
        #change turn
        #find winner
        


        