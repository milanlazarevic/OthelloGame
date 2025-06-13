from Othello.othello import Othello
from Othello.othelloGUI import OthelloGUI



def main():
    game = Othello()
    gui = OthelloGUI(game) 
    gui.run()
    


if "__main__" == __name__:
    main()