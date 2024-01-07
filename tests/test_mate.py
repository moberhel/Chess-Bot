from main import State
from main import Piece
import pygame


class TestKing():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Chess") 
    s = 400
    display = pygame.display.set_mode((s, s))
    state = State()

    def test_checkmate1(self):
        self.state.wk = (7,6) 
        self.state.board = [
        [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            ["br"," "," "," "," "," "," "," "],
            ["br"," "," "," "," "," ","wk"," "]
        ]
        self.state.white = True
        self.state.ifCheckmate()
        assert self.state.checkmate == True

    def test_checkmate2(self):
        self.state.bk = (7,6) 
        self.state.board = [
        [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," ","wb"],
            [" "," "," "," "," "," ","wq"," "],
            [" "," "," "," "," "," ","bk"," "]
        ]
        self.state.white = False
        self.state.ifCheckmate()
        assert self.state.checkmate == True

    def test_stalemate(self):
        self.state.bk = (1,1) 
        self.state.wk = (6,6) 
        self.state.board = [
            [" "," "," "," "," "," "," "," "],
            [" ","bk"," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," ","wk"," "],
            [" "," "," "," "," "," "," "," "]
        ]
        self.state.white = True
        self.state.ifStalemate()
        assert self.state.stalemate == True