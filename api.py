import robot_pb2
import robot_pb2_grpc
from errors import OrderError
from robot import Labyrinth, Robot


class PathFinderServicer(robot_pb2_grpc.PathFinderServicer):
    async def SetField(self, request, context):
        labyrinth = Labyrinth(height=request.N, width=request.M, grid=request.grid)
        self.robot = Robot(request.source, labyrinth)
        return robot_pb2.Empty()

    async def Moving(self, request_iterator, context):
        if not hasattr(self, "robot"):
            raise OrderError(
                "Commands were made in not right order. Make SetField at first."
            )

        async for request in request_iterator:
            move = self.robot.find_moving_and_move(request.targets)
            yield robot_pb2.MoveResponse(direction=move)
