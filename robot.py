from itertools import permutations
from typing import List, Tuple

import robot_pb2
from graph_utils import parse_goals, astar
from robot_pb2 import DOWN, UP, RIGHT, LEFT, FINISH


class Labyrinth:
    def __init__(self, height: int, width: int, grid: str):
        self.labyrinth = self._create_labyrinth(height, width, grid)

    def __len__(self):
        return len(self.labyrinth)

    def __getitem__(self, item):
        return self.labyrinth[item]

    def __repr__(self):
        output = "\n"
        for lab in self.labyrinth:
            output += str(lab) + "\n"
        return output

    def _create_labyrinth(self, height, width, grid):
        self.validate_grid(height, width, grid)

        labyrinth = [
            list(map(int, grid[i : i + width])) for i in range(0, len(grid), width)
        ]

        return labyrinth

    @staticmethod
    def validate_grid(height, width, grid):
        if len(grid) != height * width:
            raise ValueError(
                f"Grid has wrong size: Grid size: {len(grid)}\nHeight: {height}\nWidth: {width}"
            )


class Robot:
    def __init__(self, position: robot_pb2.Point, labyrinth):
        self.coordinate_i = position.i
        self.coordinate_j = position.j
        self.labyrinth = labyrinth
        self.robot_position = (self.coordinate_i, self.coordinate_j)
        self.goals = None
        self.optimal_path = None

    def find_moving_and_move(self, goals: List[robot_pb2.Point]):
        goals: List[Tuple[int, int]] = parse_goals(goals)

        # Check goals equal with last one request
        if not self.goals_are_equal(goals):
            self.goals = goals
            self.optimal_path = self._find_best_path(self.goals)
        next_step = self.get_next_step()
        return self._get_moving_enum_and_move(next_step)

    def get_next_step(self) -> Tuple[int, int] | None:
        """Get netx step from optimal path"""
        return self.optimal_path.pop(0) if self.optimal_path else None

    def goals_are_equal(self, goals):
        """Are goals equal"""
        if self.goals is None:
            return False
        return set(self.goals) == set(goals)

    def _move(self, next_step: Tuple[int, int]):
        """Change robot coordinates"""
        self.coordinate_i, self.coordinate_j = next_step
        self.robot_position = (self.coordinate_i, self.coordinate_j)

    def _get_moving_enum_and_move(self, next_step: Tuple[int, int] | None):
        """Get enum str for MoveResponse"""
        if next_step is None:
            return FINISH

        coordinate_i, coordinate_j = next_step
        if coordinate_i > self.coordinate_i:
            motion = DOWN
        elif coordinate_i < self.coordinate_i:
            motion = UP
        elif coordinate_j > self.coordinate_j:
            motion = RIGHT
        elif coordinate_j < self.coordinate_j:
            motion = LEFT

        self._move(next_step)
        return motion

    def _find_best_path(self, goals: List[Tuple[int, int]]):
        optimal_path = None
        min_distance = float("inf")

        for permutation in permutations(goals):
            total_distance = 0
            path = []
            start = self.robot_position  # Начальная точка для каждой перестановки
            for end in permutation:
                partial_path = astar(self.labyrinth, start, end)
                if not partial_path:
                    break  # Если не удалось найти путь между точками, прерываем поиск

                path.extend(
                    partial_path[1:]
                )  # Расширяем полный путь, исключая начальную точку
                total_distance += len(partial_path) - 1

                start = end  # Новая начальная точка для следующего шага

            if total_distance < min_distance:
                min_distance = total_distance
                optimal_path = path

        return optimal_path
