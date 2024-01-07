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
    state.board = [
        [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," ","bk"," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," ","wk"," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," ","wp"],
            [" "," "," "," "," "," "," "," "]
    ]

    def test_King1(self):
        self.state.white = True
        old = (3,3)
        new = (2,3)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_King2(self):
        self.state.white = True
        old = (3,3)
        new = (2,2)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_King3(self):
        self.state.white = True
        old = (3,3)
        new = (2,4)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_King4(self):
        self.state.white = True
        old = (3,3)
        new = (3,2)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_King5(self):
        self.state.white = True
        old = (3,3)
        new = (3,4)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_King6(self):
        self.state.white = True
        old = (3,3)
        new = (4,2)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_King7(self):
        self.state.white = True
        old = (3,3)
        new = (4,3)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_King8(self):
        self.state.white = True
        old = (3,3)
        new = (4,4)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        assert self.state.board[new[0]][new[1]] == piece
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])
