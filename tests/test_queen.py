from main import State
from main import Piece
import pygame

class TestQueen():
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
            [" "," "," ","wq"," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "]
    ]

    def test_Queen1(self):
        self.state.white = True
        old = (3,3)
        new = (5,3)
        piece = self.state.board[old[0]][old[1]]
        queen = Piece(old, new, self.state.board) 
        self.state.movePiece(queen, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_Queen2(self):
        self.state.white = True
        old = (3,3)
        new = (2,2)
        piece = self.state.board[old[0]][old[1]]
        queen = Piece(old, new, self.state.board) 
        self.state.movePiece(queen, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_Queen3(self):
        self.state.white = True
        old = (3,3)
        new = (1,5)
        piece = self.state.board[old[0]][old[1]]
        queen = Piece(old, new, self.state.board) 
        self.state.movePiece(queen, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_Queen4(self):
        self.state.white = True
        old = (3,3)
        new = (3,7)
        piece = self.state.board[old[0]][old[1]]
        queen = Piece(old, new, self.state.board) 
        self.state.movePiece(queen, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_Queen5(self):
        self.state.white = True
        old = (3,3)
        new = (3,6)
        piece = self.state.board[old[0]][old[1]]
        queen = Piece(old, new, self.state.board) 
        self.state.movePiece(queen, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_Queen6(self):
        self.state.white = True
        old = (3,3)
        new = (6,0)
        piece = self.state.board[old[0]][old[1]]
        queen = Piece(old, new, self.state.board) 
        self.state.movePiece(queen, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_Queen7(self):
        self.state.white = True
        old = (3,3)
        new = (5,3)
        piece = self.state.board[old[0]][old[1]]
        queen = Piece(old, new, self.state.board) 
        self.state.movePiece(queen, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_Queen8(self):
        self.state.white = True
        old = (3,3)
        new = (7,7)
        piece = self.state.board[old[0]][old[1]]
        queen = Piece(old, new, self.state.board) 
        self.state.movePiece(queen, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])