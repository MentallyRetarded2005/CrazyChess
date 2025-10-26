from typing import Dict, Tuple, Optional, List
from pieces import ChessPiece, Rook, Knight, Bishop, Queen, King, Pawn


class ChessBoard:
    SIZE = 8

    def __init__(self) -> None:
        self._board_state = {(x, y): None
                            for x in range(self.SIZE)
                            for y in range(self.SIZE)}
        self._white_pieces = []
        self._black_pieces = []
        self.place_pieces()

    @property
    def board_state(self) -> Dict[Tuple[int, int], Optional[ChessPiece]]:
        return self._board_state

    @board_state.setter
    def board_state(self, new_pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]]) -> None:
        self._board_state = new_pieces_pos

    @property
    def white_pieces(self) -> List[ChessPiece]:
        return self._white_pieces

    @white_pieces.setter
    def white_pieces(self, pieces: List[ChessPiece]) -> None:
        self._white_pieces = pieces

    @property
    def black_pieces(self) -> List[ChessPiece]:
        return self._black_pieces

    @black_pieces.setter
    def black_pieces(self, pieces: List[ChessPiece]) -> None:
        self._black_pieces = pieces

    def place_pieces(self):
        # Pawns
        for x in range(self.SIZE):
            black_pawn = Pawn(x, 1, "black")
            self.board_state[(x, 1)] = black_pawn
            self.black_pieces.append(black_pawn)

            white_pawn = Pawn(x, 6, "white")
            self.board_state[(x, 6)] = white_pawn
            self.white_pieces.append(white_pawn)

        # Rooks
        black_rook1 = Rook(0, 0, "black")
        black_rook2 = Rook(7, 0, "black")
        self.board_state[(0, 0)] = black_rook1
        self.board_state[(7, 0)] = black_rook2
        self.black_pieces.extend((black_rook1, black_rook2))

        white_rook1 = Rook(0, 7, "white")
        white_rook2 = Rook(7, 7, "white")
        self.board_state[(0, 7)] = white_rook1
        self.board_state[(7, 7)] = white_rook2
        self.white_pieces.extend((white_rook1, white_rook2))

        # Knights
        black_knight1 = Knight(1, 0, "black")
        black_knight2 = Knight(6, 0, "black")
        self.board_state[(1, 0)] = black_knight1
        self.board_state[(6, 0)] = black_knight2
        self.black_pieces.extend((black_knight1, black_knight2))

        white_knight1 = Knight(1, 7, "white")
        white_knight2 = Knight(6, 7, "white")
        self.board_state[(1, 7)] = white_knight1
        self.board_state[(6, 7)] = white_knight2
        self.white_pieces.extend((white_knight1, white_knight2))

        # Bishops
        black_bishop1 = Bishop(2, 0, "black")
        black_bishop2 = Bishop(5, 0, "black")
        self.board_state[(2, 0)] = black_bishop1
        self.board_state[(5, 0)] = black_bishop2
        self.black_pieces.extend((black_bishop1, black_bishop2))

        white_bishop1 = Bishop(2, 7, "white")
        white_bishop2 = Bishop(5, 7, "white")
        self.board_state[(2, 7)] = white_bishop1
        self.board_state[(5, 7)] = white_bishop2
        self.white_pieces.extend((white_bishop1, white_bishop2))

        # Queens
        black_queen = Queen(3, 0, "black")
        self.board_state[(3, 0)] = black_queen
        self.black_pieces.append(black_queen)

        white_queen = Queen(3, 7, "white")
        self.board_state[(3, 7)] = white_queen
        self.white_pieces.append(white_queen)

        # Kings
        black_king = King(4, 0, "black")
        self.board_state[(4, 0)] = black_king
        self.black_pieces.append(black_king)

        white_king = King(4, 7, "white")
        self.board_state[(4, 7)] = white_king
        self.white_pieces.append(white_king)