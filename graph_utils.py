import heapq
from typing import List, Tuple

from robot_pb2 import Point


def astar(labyrinth, start, end) -> List[Tuple[int, int]] | None:
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end:
            path = reconstruct_path(came_from, end)
            return path
        for neighbor in get_neighbors(current, labyrinth):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score, neighbor))

    return None


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def get_neighbors(node, labyrinth):
    neighbors = []
    for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_node = (node[0] + i, node[1] + j)

        if (
            0 <= new_node[1] < len(labyrinth[0])
            and len(labyrinth) > new_node[0] >= 0 == labyrinth[new_node[0]][new_node[1]]
        ):
            neighbors.append(new_node)
    return neighbors


def parse_goals(goals: List[Point]):
    return [(goal.i, goal.j) for goal in goals]
