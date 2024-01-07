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
        ["br"," "," ","bk"," "," "," ","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr"," "," ","wk"," "," "," ","wr"]
    ]

    def test_Castle1(self):
        self.state.white = True
        old = (7,3)
        new = (7,1)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        self.state.checkCastle(piece, new[0], new[1])
        assert self.state.board[new[0]][new[1]] == piece and self.state.board[new[0]][new[1]+1] == "wr"
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_Castle2(self):
        self.state.white = True
        old = (7,3)
        new = (7,5)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        self.state.checkCastle(piece, new[0], new[1])
        assert self.state.board[new[0]][new[1]] == piece and self.state.board[new[0]][new[1]-1] == "wr"
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_Castle3(self):
        self.state.white = False
        old = (0,3)
        new = (0,5)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board) 
        self.state.movePiece(king, self.display)
        self.state.checkCastle(piece, new[0], new[1])
        assert self.state.board[new[0]][new[1]] == piece and self.state.board[new[0]][new[1]-1] == "br"
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])

    def test_Castle4(self):
        self.state.white = False
        old = (0,3)
        new = (0,1)
        piece = self.state.board[old[0]][old[1]]
        king = Piece(old, new, self.state.board)
        self.state.movePiece(king, self.display)
        self.state.checkCastle(piece, new[0], new[1])
        assert self.state.board[new[0]][new[1]] == piece and self.state.board[new[0]][new[1]+1] == "br"
        self.state.Undo(old[0], old[1], piece, " ", new[0], new[1])
