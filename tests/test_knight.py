from main import State
from main import Piece
import pygame

class TestKnight():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Chess") 
    s = 400
    display = pygame.display.set_mode((s, s))
    state = State()
    state.board = [
        [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," ","wn","wn","bn","bn"," "," "],
            [" "," ","wn","wn","bn","bn"," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "]
    ]

    def test_Knight1(self):
        self.state.white = True
        old = (3,2)
        new = (2,0)
        piece = self.state.board[old[0]][old[1]]
        knight = Piece(old, new, self.state.board) 
        self.state.movePiece(knight, self.display)
        assert self.state.board[new[0]][new[1]] == piece

    def test_Knight2(self):
        self.state.white = True
        old = (4,2)
        new = (5,0)
        piece = self.state.board[old[0]][old[1]]
        knight = Piece(old, new, self.state.board) 
        self.state.movePiece(knight, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        
    def test_Knight3(self):
        self.state.white = True
        old = (3,3)
        new = (1,2)
        piece = self.state.board[old[0]][old[1]]
        knight = Piece(old, new, self.state.board) 
        self.state.movePiece(knight, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        
    def test_Knight4(self):
        self.state.white = True
        old = (4,3)
        new = (6,2)
        piece = self.state.board[old[0]][old[1]]
        knight = Piece(old, new, self.state.board) 
        self.state.movePiece(knight, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        
    def test_Knight5(self):
        self.state.white = False
        old = (3,4)
        new = (1,5)
        piece = self.state.board[old[0]][old[1]]
        knight = Piece(old, new, self.state.board) 
        self.state.movePiece(knight, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        
    def test_Knight6(self):
        self.state.white = False
        old = (4,4)
        new = (6,5)
        piece = self.state.board[old[0]][old[1]]
        knight = Piece(old, new, self.state.board) 
        self.state.movePiece(knight, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        
    def test_Knight7(self):
        self.state.white = False
        old = (3,5)
        new = (2,7)
        piece = self.state.board[old[0]][old[1]]
        knight = Piece(old, new, self.state.board) 
        self.state.movePiece(knight, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        
    def test_Knight8(self):
        self.state.white = False
        old = (4,5)
        new = (5,7)
        piece = self.state.board[old[0]][old[1]]
        knight = Piece(old, new, self.state.board) 
        self.state.movePiece(knight, self.display)
        assert self.state.board[new[0]][new[1]] == piece
