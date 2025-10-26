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

    def move_to(self, new_x: int, new_y: int) -> None:
        self.x = new_x
        self.y = new_y

    @abstractmethod
    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int], Optional['ChessPiece']],
                           enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece'],
                           own_king: 'King') -> List[Tuple[int, int]]:
        pass

    @abstractmethod
    def attack_range(self, pieces_pos: Dict[Tuple[int, int], Optional['ChessPiece']]) -> List[Tuple[int, int]]:
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

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]],
                           enemy_pieces: List[ChessPiece], own_pieces: List[ChessPiece],
                           own_king: 'King') -> List[Tuple[int, int]]:
        possible_moves = []
        directions = ((0, -1), (0, 1), (-1, 0), (1, 0))

        for dx, dy in directions:
            step = 1
            while True:
                new_x = self.x + step * dx
                new_y = self.y + step * dy
                if not self.field_exists(x=new_x, y=new_y):
                    break

                target_piece = pieces_pos.get((new_x, new_y))
                if (target_piece is not None) and (target_piece.color == self.color):
                    break

                new_pieces_pos = pieces_pos.copy()
                new_pieces_pos[(self.x, self.y)] = None
                new_pieces_pos[(new_x, new_y)] = self
                if not own_king.is_king_in_check(pieces_pos=new_pieces_pos, enemy_pieces=enemy_pieces,
                                                 king_x=own_king.x, king_y=own_king.y):
                    possible_moves.append((new_x, new_y))

                if (target_piece is not None) and (target_piece != self.color):
                    break
                step += 1
        return possible_moves

    def attack_range(self, pieces_pos: Dict[Tuple[int, int], Optional['ChessPiece']]) -> List[Tuple[int, int]]:
        attack_positions = []
        directions = ((0, -1), (0, 1), (-1, 0), (1, 0))

        for dx, dy in directions:
            step = 1
            while True:
                new_x = self.x + step * dx
                new_y = self.y + step * dy
                if not self.field_exists(x=new_x, y=new_y):
                    break

                target_piece = pieces_pos.get((new_x, new_y))
                if target_piece is not None:
                    if target_piece.color != self.color:
                        attack_positions.append((new_x, new_y))
                    break

                attack_positions.append((new_x, new_y))
                step += 1

        return attack_positions



class Knight(ChessPiece):
    def __init__(self, start_x: int, start_y: int, color: str):
        super().__init__(start_x=start_x, start_y=start_y, color=color)

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]],
                           enemy_pieces: List[ChessPiece], own_pieces: List[ChessPiece],
                           own_king: 'King') -> List[Tuple[int, int]]:
        possible_moves = []
        directions = ((1, 2), (-1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1))

        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            if not self.field_exists(x=new_x, y=new_y):
                continue

            target_piece = pieces_pos.get((new_x, new_y))
            if (target_piece is not None) and (target_piece.color == self.color):
                continue

            new_pieces_pos = pieces_pos.copy()
            new_pieces_pos[(self.x, self.y)] = None
            new_pieces_pos[(new_x, new_y)] = self
            if not own_king.is_king_in_check(pieces_pos=new_pieces_pos, enemy_pieces=enemy_pieces,
                                             king_x=own_king.x, king_y=own_king.y):
                possible_moves.append((new_x, new_y))
        return possible_moves

    def attack_range(self, pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]]) -> List[Tuple[int, int]]:
        attack_positions = []
        directions = ((1, 2), (-1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1))

        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            if not self.field_exists(x=new_x, y=new_y):
                continue

            target_piece = pieces_pos.get((new_x, new_y))
            if (target_piece is not None) and (target_piece.color == self.color):
                continue

            attack_positions.append((new_x, new_y))

        return attack_positions


class Bishop(ChessPiece):
    def __init__(self, start_x: int, start_y: int, color: str):
        super().__init__(start_x=start_x, start_y=start_y, color=color)

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]],
                           enemy_pieces: List[ChessPiece], own_pieces: List[ChessPiece],
                           own_king: 'King') -> List[Tuple[int, int]]:
        possible_moves = []
        directions = (-1, 1)

        for dx in directions:
            for dy in directions:
                step = 1
                while True:
                    new_x = self.x + step * dx
                    new_y = self.y + step * dy
                    if not self.field_exists(x=new_x, y=new_y):
                        break

                    target_piece = pieces_pos.get((new_x, new_y))
                    if (target_piece is not None) and (target_piece.color == self.color):
                        break

                    new_pieces_pos = pieces_pos.copy()
                    new_pieces_pos[(self.x, self.y)] = None
                    new_pieces_pos[(new_x, new_y)] = self
                    if not own_king.is_king_in_check(pieces_pos=new_pieces_pos, enemy_pieces=enemy_pieces,
                                                     king_x=own_king.x, king_y=own_king.y):
                        possible_moves.append((new_x, new_y))

                    if (target_piece is not None) and (target_piece != self.color):
                        break
                    step += 1
        return possible_moves

    def attack_range(self, pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]]) -> List[Tuple[int, int]]:
        attack_positions = []
        directions = (-1, 1)

        for dx in directions:
            for dy in directions:
                step = 1
                while True:
                    new_x = self.x + step * dx
                    new_y = self.y + step * dy
                    if not self.field_exists(x=new_x, y=new_y):
                        break

                    target_piece = pieces_pos.get((new_x, new_y))
                    if target_piece is not None:
                        if target_piece.color != self.color:
                            attack_positions.append((new_x, new_y))
                        break

                    attack_positions.append((new_x, new_y))
                    step += 1

        return attack_positions


class Queen(ChessPiece):
    def __init__(self, start_x: int, start_y: int, color: str):
        super().__init__(start_x=start_x, start_y=start_y, color=color)

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]],
                           enemy_pieces: List[ChessPiece], own_pieces: List[ChessPiece],
                           own_king: 'King') -> List[Tuple[int, int]]:
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
                    if (target_piece is not None) and (target_piece.color == self.color):
                        break

                    new_pieces_pos = pieces_pos.copy()
                    new_pieces_pos[(self.x, self.y)] = None
                    new_pieces_pos[(new_x, new_y)] = self
                    if not own_king.is_king_in_check(pieces_pos=new_pieces_pos, enemy_pieces=enemy_pieces,
                                                     king_x=own_king.x, king_y=own_king.y):
                        possible_moves.append((new_x, new_y))

                    if (target_piece is not None) and (target_piece != self.color):
                        break
                    step += 1
        return possible_moves

    def attack_range(self, pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]]) -> List[Tuple[int, int]]:
        attack_positions = []
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
                    if target_piece is not None:
                        if target_piece.color != self.color:
                            attack_positions.append((new_x, new_y))
                        break

                    attack_positions.append((new_x, new_y))
                    step += 1

        return attack_positions


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

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]],
                           enemy_pieces: List[ChessPiece], own_pieces: List[ChessPiece],
                           own_king: 'King') -> List[Tuple[int, int]]:
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
                if (target_piece is None) or \
                        (target_piece is not None and target_piece.color != self.color):

                    new_pieces_pos = pieces_pos.copy()
                    new_pieces_pos[(self.x, self.y)] = None
                    new_pieces_pos[(new_x, new_y)] = self
                    if not self.is_king_in_check(pieces_pos=new_pieces_pos, enemy_pieces=enemy_pieces,
                                                 king_x=new_x, king_y=new_y):
                        possible_moves.append((new_x, new_y))

        if self.can_short_castle(pieces_pos=pieces_pos, enemy_pieces=enemy_pieces):
            possible_moves.append((self.x + 2, self.y))
        if self.can_long_castle(pieces_pos=pieces_pos, enemy_pieces=enemy_pieces):
            possible_moves.append((self.x - 2, self.y))
        return possible_moves

    def attack_range(self, pieces_pos: Dict[Tuple[int, int], Optional['ChessPiece']]) -> List[Tuple[int, int]]:
        attack_positions = []
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
                if (target_piece is not None) and (target_piece.color == self.color):
                    continue
                attack_positions.append((new_x, new_y))
        return attack_positions

    @staticmethod
    def is_king_in_check(pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]],
                         enemy_pieces: List[ChessPiece], king_x: int, king_y: int) -> bool:
        for piece in enemy_pieces:
            attack_range = piece.attack_range(pieces_pos)
            if (king_x, king_y) in attack_range:
                return True
        return False

    def can_short_castle(self, pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]],
                         enemy_pieces: List[ChessPiece]) -> bool:
        if self.has_moved:
            return False

        if (pieces_pos[(self.x + 1, self.y)] is not None) or \
                (pieces_pos[(self.x + 2, self.y)] is not None):
            return False

        rook = pieces_pos[(self.x + 3, self.y)]
        if (rook is None) or rook.has_moved:
            return False

        if self.is_king_in_check(pieces_pos, enemy_pieces, self.x + 1, self.y) or \
                self.is_king_in_check(pieces_pos, enemy_pieces, self.x + 2, self.y):
            return False
        return True

    def can_long_castle(self, pieces_pos: Dict[Tuple[int, int], Optional[ChessPiece]],
                        enemy_pieces: List[ChessPiece]) -> bool:
        if self.has_moved:
            return False

        if (pieces_pos[(self.x - 1, self.y)] is not None) or \
                (pieces_pos[(self.x - 2, self.y)] is not None) or \
                (pieces_pos[(self.x - 3, self.y)] is not None):
            return False

        rook = pieces_pos[(self.x - 4, self.y)]
        if (rook is None) or rook.has_moved:
            return False

        if self.is_king_in_check(pieces_pos, enemy_pieces, self.x - 1, self.y) or \
                self.is_king_in_check(pieces_pos, enemy_pieces, self.x - 2, self.y):
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

    def get_possible_moves(self, pieces_pos: Dict[Tuple[int, int], Optional['ChessPiece']],
                           enemy_pieces: List['ChessPiece'], own_pieces: List['ChessPiece'],
                           own_king: 'King') -> List[Tuple[int, int]]:
        pass

    def attack_range(self, pieces_pos: Dict[Tuple[int, int], Optional['ChessPiece']]) -> List[Tuple[int, int]]:
        pass

    def is_en_passant_avaible(self, pieces_pos: Dict[Tuple[int, int], Optional['ChessPiece']],
                              last_move: ChessPiece) -> bool:
        pass