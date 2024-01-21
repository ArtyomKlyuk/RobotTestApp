from unittest.mock import MagicMock

import pytest

import robot_pb2
from robot import Labyrinth, Robot


@pytest.fixture
def mock_astar(monkeypatch):
    mock_astar = MagicMock()
    monkeypatch.setattr("graph_utils.astar", mock_astar)
    return mock_astar


def test_create_labyrinth():
    # Тестирование успешного создания лабиринта
    height, width, grid = 3, 3, "010001000"
    labyrinth = Labyrinth(height, width, grid)
    assert len(labyrinth) == height
    assert labyrinth[0][0] == 0
    assert labyrinth[2][2] == 0


def test_create_labyrinth_invalid_grid():
    # Тестирование ошибки при создании лабиринта с неверным размером сетки
    with pytest.raises(ValueError):
        Labyrinth(3, 3, "01000100")


def test_get_next_step():
    # Тестирование метода get_next_step
    labyrinth = Labyrinth(3, 3, "010001000")
    robot = Robot(robot_pb2.Point(i=0, j=0), labyrinth)

    robot.optimal_path = [(0, 1), (1, 1), (2, 1)]

    next_step = robot.get_next_step()

    assert next_step == (0, 1)


def test_goals_are_equal():
    # Тестирование метода goals_are_equal
    labyrinth = Labyrinth(3, 3, "010001000")
    robot = Robot(robot_pb2.Point(i=0, j=0), labyrinth)

    # Задаем goals
    robot.goals = [(1, 1), (2, 2)]

    # Проверяем, что метод возвращает True для идентичных goals
    assert robot.goals_are_equal([(2, 2), (1, 1)])

    # Проверяем, что метод возвращает False для различных goals
    assert not robot.goals_are_equal([(1, 1), (0, 0)])


def test_move():
    # Тестирование метода _move
    labyrinth = Labyrinth(3, 3, "010001000")
    robot = Robot(robot_pb2.Point(i=0, j=0), labyrinth)

    robot._move((2, 2))

    assert robot.coordinate_i == 2
    assert robot.coordinate_j == 2
    assert robot.robot_position == (2, 2)


def test_get_moving_enum_and_move():
    # Тестирование метода _get_moving_enum_and_move
    labyrinth = Labyrinth(3, 3, "010001000")
    robot = Robot(robot_pb2.Point(i=0, j=0), labyrinth)

    result = robot._get_moving_enum_and_move((1, 0))

    assert result == robot_pb2.DOWN
    assert robot.coordinate_i == 1
    assert robot.coordinate_j == 0
