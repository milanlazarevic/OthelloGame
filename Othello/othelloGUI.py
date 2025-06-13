import copy
import time
import pygame
import sys
from Othello.othello import Player
from Othello.othello import Othello
from Othello.computer import Computer

class OthelloGUI():
    def __init__(self, game):
        # Initialize Pygame
        pygame.init()
        self.game = game
        
        # Define constants
        self.WIDTH = 400
        self.HEIGHT = 450
        self.CELL_SIZE = 50
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (33, 212, 164)
        self.GRAY = (105, 109, 128)
        self.FONT_SIZE = 32
       
        # self.disc_counts = {"black": 2, "white": 2}
        # self.board = [
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 1, -1, 0, 0, 0],
        #     [0, 0, 0, -1, 1, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0]
        # ]

        # Create the game window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Othello game")
        self.font = pygame.font.Font(None, self.FONT_SIZE)

    def draw_board(self):
        self.screen.fill(self.GREEN)
        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                if self.game.table[row][col] == 1:
                    pygame.draw.circle(self.screen, self.BLACK, rect.center, self.CELL_SIZE // 2 - 2)
                elif self.game.table[row][col] == -1:
                    pygame.draw.circle(self.screen, self.WHITE, rect.center, self.CELL_SIZE // 2 - 2)
    def draw_posible_moves(self,game):
        possibleMoves = self.game.find_legal_moves(game.currPlayer)
        for i in possibleMoves:
            rect = pygame.Rect(i[1] * self.CELL_SIZE, i[0] * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.circle(self.screen, self.GRAY, rect.center, self.CELL_SIZE // 2 - 2,1,)
    def display_disc_counts(self):
        text_white = self.font.render(f"White: {self.game.disc_count[Player.white]}", True, self.WHITE)
        text_black = self.font.render(f"Black: {self.game.disc_count[Player.black]}", True, self.BLACK)
        self.screen.blit(text_white, (10, 410))  # Top-left corner
        self.screen.blit(text_black, (300, 410))  # Below the previous text

    def run(self):
        while True:
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.game.currPlayer == Player.black:
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // self.CELL_SIZE
                        row = pos[1] // self.CELL_SIZE
                        [legal, outflanked] = self.game.is_move_legal(self.game.currPlayer, (row,col), [])
                        if legal:
                            self.game.table, over= self.game.make_move(self.game.currPlayer, (row,col), outflanked)
                           
                            if self.game.is_table_full():
                                self.game.game_over = True
                            # prethodna_tabla = copy.deepcopy(self.board)
                            prethodni_broj_crnih = copy.deepcopy(self.game.disc_count[Player.black])
                            prethodni_broj_bijelih = copy.deepcopy(self.game.disc_count[Player.white])
                            
                            # potez racunara kao bijelog
                            bot = Computer(self.game)
                            best_move, outflankedByBot = bot.get_best_move(self.game.table)
                            
                            # self.board = prethodna_tabla
                            # self.game.currPlayer = Player.white
                            # self.game.table = prethodna_tabla
                            
                            # self.game.game_over = True
                            
                            self.game.disc_count[Player.white] = prethodni_broj_bijelih
                            self.game.disc_count[Player.black] = prethodni_broj_crnih
                            if best_move is None:
                                self.game.game_over = True
                                break
                            self.game.table, self.game.game_over = self.game.make_move(self.game.currPlayer, best_move, outflankedByBot)
                            if self.game.is_table_full():
                                self.game.game_over = True
                            if self.game.game_over == True:
                                print("kkk")
                                break
                            # print("potez racunara kao bijelog")
                        else:
                            print("potez nije validan") 
                if self.game.currPlayer == Player.white:
                    bot = Computer(self.game)
                    best_move, outflankedByBot = bot.get_best_move(self.game.table)
                            
                            # self.board = prethodna_tabla
                            # self.game.currPlayer = Player.white
                            # self.game.table = prethodna_tabla
                            
                            # self.game.game_over = True
                            
                    # self.game.disc_count[Player.white] = prethodni_broj_bijelih
                    # self.game.disc_count[Player.black] = prethodni_broj_crnih
                    if best_move is None:
                        self.game.game_over = True
                        break
                    self.game.table, self.game.game_over = self.game.make_move(self.game.currPlayer, best_move, outflankedByBot)
                    if self.game.is_table_full():
                        self.game.game_over = True
                        break
                    if self.game.game_over == True:
                        print("milan")
                
                k = self.game.find_legal_moves(self.game.currPlayer)
                if self.game.find_legal_moves(self.game.currPlayer) == {}:
                    self.game.game_over = True
                    break
                if self.game.find_legal_moves(self.game.nextPlayer) == {}:
                    self.game.game_over = True
                    break

                if self.game.is_table_full():
                    self.game.game_over = True
                    break

                if self.game.game_over == True:
                    if self.game.find_winner() == Player.black:
                        print(  "Black is the winner" )
                    elif self.game.find_winner() == Player.white:
                        print(  "White is the winner" )
                    else:
                        print(  "It's a tie!")
                    time.sleep(5)
                    print("game over")
                    pygame.quit()
                    sys.exit()
                    
                        
                        

            # Draw the board
            self.draw_board()
            self.draw_posible_moves(self.game)
            # Display Disc Counts
            self.display_disc_counts()

            # Update the display
            pygame.display.flip()


