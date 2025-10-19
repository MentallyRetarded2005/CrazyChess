from abc import ABC, abstractmethod
from typing import Tuple, List


class ChessPiece(ABC):
    def __init__(self, start_pos: Tuple[int, int], color: str) -> None:
        self.__pos = start_pos
        self.__color = color
        self.__possible_moves = []

    @property
    def pos(self) -> Tuple[int, int]:
        return self.__pos

    @pos.setter
    def pos(self, new_pos: Tuple[int, int]) -> None:
        self.__pos = new_pos

    @property
    def color(self) -> str:
        return self.__color

    @property
    def possible_moves(self) -> List[Tuple[int, int]]:
        return self.__possible_moves

    @possible_moves.setter
    def possible_moves(self, moves: List[Tuple[int, int]]) -> None:
        self.__possible_moves = moves

    @abstractmethod
    def check_possible_moves(self, pieces_pos) -> List[Tuple[int, int]]:
        pass

    @abstractmethod
    def is_move_possible(self, new_pos: Tuple[int, int]) -> bool:
        pass

    @abstractmethod
    def move_to(self, new_pos: Tuple[int, int]) -> None:
        pass


class Pawn(ChessPiece):
    def __init__(self, pos: Tuple[int, int], color: str) -> None:
        super().__init__(pos, color)
        self.__direction = -1 if self.color == 'white' else 1
        self.__has_moved = False

    @property
    def direction(self) -> bool:
        return self.__direction

    @property
    def has_moved(self) -> bool:
        return self.__has_moved

    @has_moved.setter
    def has_moved(self, moved: bool) -> None:
        self.__has_moved = moved

    # TODO: Реализовать переопределённые методы
    def check_possible_moves(self, pieces_pos) -> List[Tuple[int, int]]:
        pass

    def is_move_possible(self, new_pos: Tuple[int, int]) -> bool:
        pass

    def move_to(self, new_pos: Tuple[int, int]) -> None:
        pass