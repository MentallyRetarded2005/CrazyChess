from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional, List


class ChessPiece(ABC):
    def __init__(self, start_x: int, start_y: int, color: str) -> None:
        self._x = start_x
        self._y = start_y
        self._color = color

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, new_x: int) -> None:
        self._x = new_x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, new_y: int) -> None:
        self._y = new_y

    @property
    def color(self) -> str:
        return self._color

    @staticmethod
    def field_exists(x: int, y: int) -> bool:
        return (0 <= x <= 7) and (0 <= y <= 7)

    @staticmethod
    def has_piece(piece: Optional['ChessPiece']) -> bool:
        return piece is not None

    def is_own_piece(self, piece: 'ChessPiece') -> bool:
        return piece.color == self.color

    def move_to(self, new_x: int, new_y: int) -> None:
        self.x = new_x
        self.y = new_y

    @abstractmethod
    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                           enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece'],
                           own_king: 'King', only_attacking_moves: bool = False) \
            -> List[Tuple[int, int]]:
        pass


class Rook(ChessPiece):
    def __init__(self, start_x: int, start_y: int, color: str) -> None:
        super().__init__(start_x=start_x, start_y=start_y, color=color)
        self._has_moved = False

    @property
    def has_moved(self) -> bool:
        return self._has_moved

    def move_to(self, new_x: int, new_y: int) -> None:
        if not self.has_moved:
            self._has_moved = True
        super().move_to(new_x=new_x, new_y=new_y)

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                           enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece'],
                           own_king: 'King', only_attacking_moves: bool = False) \
            -> List[Tuple[int, int]]:
        possible_moves = []
        directions = ((0, -1), (0, 1), (-1, 0), (1, 0))

        for dx, dy in directions:
            step = 1
            while True:
                new_x = self.x + dx * step
                new_y = self.y + dy * step
                if not self.field_exists(x=new_x, y=new_y):
                    break

                target_piece = pieces_pos.get((new_x, new_y))

                if only_attacking_moves:
                    if self.has_piece(piece=target_piece):
                        if not self.is_own_piece(piece=target_piece):
                            possible_moves.append((new_x, new_y))
                        break
                    possible_moves.append((new_x, new_y))
                else:
                    if self.has_piece(piece=target_piece) and \
                            self.is_own_piece(piece=target_piece):
                        break

                    new_pieces_pos = pieces_pos.copy()
                    new_pieces_pos[(self.x, self.y)] = None
                    new_pieces_pos[(new_x, new_y)] = self
                    if not own_king.is_king_in_check(pieces_pos=new_pieces_pos,
                                                     enemy_pieces=enemy_pieces,
                                                     own_pieces=own_pieces,
                                                     king_x=own_king.x,
                                                     king_y=own_king.y):
                        possible_moves.append((new_x, new_y))

                    if self.has_piece(piece=target_piece) and \
                            not self.is_own_piece(piece=target_piece):
                        break
                step += 1

        return possible_moves


class Knight(ChessPiece):
    def __init__(self, start_x: int, start_y: int, color: str) -> None:
        super().__init__(start_x=start_x, start_y=start_y, color=color)

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                           enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece'],
                           own_king: 'King', only_attacking_moves: bool = False) \
            -> List[Tuple[int, int]]:
        possible_moves = []
        directions = ((1, 2), (1, -2), (2, 1), (2, -1),
                      (-1, 2), (-1, -2), (-2, 1), (-2, -1))

        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            if not self.field_exists(x=new_x, y=new_y):
                continue

            target_piece = pieces_pos.get((new_x, new_y))

            if only_attacking_moves:
                if self.has_piece(piece=target_piece) and \
                        self.is_own_piece(piece=target_piece):
                    continue
                possible_moves.append((new_x, new_y))
            else:
                if self.has_piece(piece=target_piece) and \
                        self.is_own_piece(piece=target_piece):
                    continue

                new_pieces_pos = pieces_pos.copy()
                new_pieces_pos[(self.x, self.y)] = None
                new_pieces_pos[(new_x, new_y)] = self
                if not own_king.is_king_in_check(pieces_pos=new_pieces_pos,
                                                 enemy_pieces=enemy_pieces,
                                                 own_pieces=own_pieces,
                                                 king_x=own_king.x,
                                                 king_y=own_king.y):
                    possible_moves.append((new_x, new_y))

        return possible_moves


class Bishop(ChessPiece):
    def __init__(self, start_x: int, start_y: int, color: str) -> None:
        super().__init__(start_x=start_x, start_y=start_y, color=color)

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                           enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece'],
                           own_king: 'King', only_attacking_moves: bool = False) \
            -> List[Tuple[int, int]]:
        possible_moves = []
        directions = (-1, 1)

        for dx in directions:
            for dy in directions:
                step = 1
                while True:
                    new_x = self.x + dx * step
                    new_y = self.y + dy * step
                    if not self.field_exists(x=new_x, y=new_y):
                        break

                    target_piece = pieces_pos.get((new_x, new_y))

                    if only_attacking_moves:
                        if self.has_piece(piece=target_piece):
                            if not self.is_own_piece(piece=target_piece):
                                possible_moves.append((new_x, new_y))
                            break
                        possible_moves.append((new_x, new_y))
                    else:
                        if self.has_piece(piece=target_piece) and \
                                self.is_own_piece(piece=target_piece):
                            break

                        new_pieces_pos = pieces_pos.copy()
                        new_pieces_pos[(self.x, self.y)] = None
                        new_pieces_pos[(new_x, new_y)] = self
                        if not own_king.is_king_in_check(pieces_pos=new_pieces_pos,
                                                         enemy_pieces=enemy_pieces,
                                                         own_pieces=own_pieces,
                                                         king_x=own_king.x,
                                                         king_y=own_king.y):
                            possible_moves.append((new_x, new_y))

                        if self.has_piece(piece=target_piece) and \
                                not self.is_own_piece(piece=target_piece):
                            break
                    step += 1

        return possible_moves


class Queen(ChessPiece):
    def __init__(self, start_x: int, start_y: int, color: str) -> None:
        super().__init__(start_x=start_x, start_y=start_y, color=color)

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                           enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece'],
                           own_king: 'King', only_attacking_moves: bool = False) \
            -> List[Tuple[int, int]]:
        possible_moves = []
        directions = (-1, 0, 1)

        for dx in directions:
            for dy in directions:
                if (dx == 0) and (dy == 0):
                    continue

                step = 1
                while True:
                    new_x = self.x + step * dx
                    new_y = self.y + step * dy
                    if not self.field_exists(x=new_x, y=new_y):
                        break

                    target_piece = pieces_pos.get((new_x, new_y))

                    if only_attacking_moves:
                        if self.has_piece(piece=target_piece):
                            if not self.is_own_piece(piece=target_piece):
                                possible_moves.append((new_x, new_y))
                            break
                        possible_moves.append((new_x, new_y))
                    else:
                        if self.has_piece(piece=target_piece) and \
                                self.is_own_piece(piece=target_piece):
                            break

                        new_pieces_pos = pieces_pos.copy()
                        new_pieces_pos[(self.x, self.y)] = None
                        new_pieces_pos[(new_x, new_y)] = self
                        if not own_king.is_king_in_check(
                                pieces_pos=new_pieces_pos,
                                enemy_pieces=enemy_pieces,
                                own_pieces=own_pieces,
                                king_x=own_king.x,
                                king_y=own_king.y):
                            possible_moves.append((new_x, new_y))

                        if self.has_piece(piece=target_piece) and \
                                not self.is_own_piece(piece=target_piece):
                            break
                    step += 1

        return possible_moves


class King(ChessPiece):
    def __init__(self, start_x: int, start_y: int, color: str) -> None:
        super().__init__(start_x, start_y, color)
        self._has_moved = False

    @property
    def has_moved(self) -> bool:
        return self._has_moved

    def move_to(self, new_x: int, new_y: int) -> None:
        if not self.has_moved:
            self._has_moved = True
        super().move_to(new_x, new_y)

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                           enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece'],
                           own_king: 'King', only_attacking_moves: bool = False) \
            -> List[Tuple[int, int]]:
        possible_moves = []
        directions = (-1, 0, 1)

        for dx in directions:
            for dy in directions:
                if (dx == 0) and (dy == 0):
                    continue

                new_x = self.x + dx
                new_y = self.y + dy
                if not self.field_exists(x=new_x, y=new_y):
                    continue

                target_piece = pieces_pos.get((new_x, new_y))

                if only_attacking_moves:
                    if self.has_piece(piece=target_piece) and \
                            self.is_own_piece(piece=target_piece):
                        continue
                    possible_moves.append((new_x, new_y))
                else:
                    if not self.has_piece(piece=target_piece) or \
                            not self.is_own_piece(piece=target_piece):

                        new_pieces_pos = pieces_pos.copy()
                        new_pieces_pos[(self.x, self.y)] = None
                        new_pieces_pos[(new_x, new_y)] = self
                        if not self.is_king_in_check(pieces_pos=new_pieces_pos,
                                                     enemy_pieces=enemy_pieces,
                                                     own_pieces=own_pieces,
                                                     king_x=new_x, king_y=new_y):
                            possible_moves.append((new_x, new_y))

        if not only_attacking_moves and not self.is_king_in_check(pieces_pos=pieces_pos,
                                                                  enemy_pieces=enemy_pieces,
                                                                  own_pieces=own_pieces,
                                                                  king_x=self.x,
                                                                  king_y=self.y):
            if self.can_short_castle(pieces_pos=pieces_pos, enemy_pieces=enemy_pieces,
                                     own_pieces=own_pieces):
                possible_moves.append((self.x + 2, self.y))
            if self.can_long_castle(pieces_pos=pieces_pos, enemy_pieces=enemy_pieces,
                                    own_pieces=own_pieces):
                possible_moves.append((self.x - 2, self.y))

        return possible_moves

    def is_king_in_check(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                         enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece'],
                         king_x: int, king_y: int) -> bool:
        for piece in enemy_pieces:
            attack_range = piece.get_possible_moves(pieces_pos=pieces_pos,
                                                    enemy_pieces=enemy_pieces,
                                                    own_pieces=own_pieces,
                                                    own_king=self,
                                                    only_attacking_moves=True)
            if (king_x, king_y) in attack_range:
                return True
        return False

    def can_short_castle(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                         enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece']) \
            -> bool:
        if self.has_moved:
            return False

        for dx in (1, 2):
            target_piece = pieces_pos[(self.x + dx, self.y)]
            if self.has_piece(piece=target_piece):
                return False

        rook = pieces_pos[(self.x + 3, self.y)]
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        if self.is_king_in_check(pieces_pos=pieces_pos, enemy_pieces=enemy_pieces,
                                 own_pieces=own_pieces, king_x=self.x + 1, king_y=self.y) or \
                self.is_king_in_check(pieces_pos=pieces_pos, enemy_pieces=enemy_pieces,
                                      own_pieces=own_pieces, king_x=self.x + 2, king_y=self.y):
            return False
        return True

    def can_long_castle(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                        enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece']) \
            -> bool:
        if self.has_moved:
            return False

        for dx in (1, 2, 3):
            target_piece = pieces_pos[(self.x - dx, self.y)]
            if self.has_piece(piece=target_piece):
                return False

        rook = pieces_pos[(self.x - 4, self.y)]
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        if self.is_king_in_check(pieces_pos=pieces_pos, enemy_pieces=enemy_pieces,
                                 own_pieces=own_pieces, king_x=self.x - 1, king_y=self.y) or \
                self.is_king_in_check(pieces_pos=pieces_pos, enemy_pieces=enemy_pieces,
                                      own_pieces=own_pieces, king_x=self.x - 2, king_y=self.y):
            return False
        return True


class Pawn(ChessPiece):
    def __init__(self, start_x: int, start_y: int, color: str) -> None:
        super().__init__(start_x, start_y, color)
        self._has_moved = False

    @property
    def has_moved(self) -> bool:
        return self._has_moved

    def move_to(self, new_x: int, new_y: int) -> None:
        if not self.has_moved:
            self._has_moved = True
        super().move_to(new_x, new_y)

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                           enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece'],
                           own_king: 'King', only_attacking_moves: bool = False) \
            -> List[Tuple[int, int]]:
        possible_moves = []
        direction = -1 if self.color == "white" else 1

        if only_attacking_moves:
            for dx in (-1, 1):
                new_x = self.x + dx
                new_y = self.y + direction
                if not self.field_exists(x=new_x, y=new_y):
                    continue

                target_piece = pieces_pos.get((new_x, new_y))
                if self.has_piece(piece=target_piece) and \
                        self.is_own_piece(piece=target_piece):
                    continue
                possible_moves.append((new_x, new_y))
        else:
            new_y1 = self.y + direction
            new_y2 = self.y + 2*direction

            # Не забыть добавить проверку условия на предпоследнюю горизонталь
            piece1 = pieces_pos[(self.x, new_y1)]
            if not self.has_piece(piece1):
                new_pieces_pos = pieces_pos.copy()
                new_pieces_pos[(self.x, self.y)] = None
                new_pieces_pos[(self.x, new_y1)] = self
                if not own_king.is_king_in_check(pieces_pos=new_pieces_pos,
                                                 enemy_pieces=enemy_pieces,
                                                 own_pieces=own_pieces,
                                                 king_x=own_king.x,
                                                 king_y=own_king.y):
                    possible_moves.append((self.x, new_y1))

            piece2 = pieces_pos[(self.x, new_y2)]
            if not self.has_moved and not self.has_piece(piece2):
                new_pieces_pos = pieces_pos.copy()
                new_pieces_pos[(self.x, self.y)] = None
                new_pieces_pos[(self.x, new_y2)] = self
                if not own_king.is_king_in_check(pieces_pos=new_pieces_pos,
                                                 enemy_pieces=enemy_pieces,
                                                 own_pieces=own_pieces,
                                                 king_x=own_king.x,
                                                 king_y=own_king.y):
                    possible_moves.append((self.x, new_y2))

            for dx in (-1, 1):
                new_x = self.x + dx
                if not self.field_exists(x=new_x, y=new_y1):
                    continue

                target_piece = pieces_pos.get((new_x, new_y1))
                if self.has_piece(piece=target_piece) and \
                        self.is_own_piece(piece=target_piece):
                    continue

                new_pieces_pos = pieces_pos.copy()
                new_pieces_pos[(self.x, self.y)] = None
                new_pieces_pos[(new_x, new_y1)] = self
                if own_king.is_king_in_check(pieces_pos=new_pieces_pos,
                                             enemy_pieces=enemy_pieces,
                                             own_pieces=own_pieces,
                                             king_x=own_king.x,
                                             king_y=own_king.y):
                    continue
                possible_moves.append((new_x, new_y1))

        return possible_moves

    def is_en_passant_avaible(self, pieces_pos: Dict[Tuple[int, int]: Optional['ChessPiece']],
                              last_move: 'ChessPiece') -> bool:
        pass