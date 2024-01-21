import asyncio
from concurrent import futures

import grpc

import robot_pb2_grpc
from api import PathFinderServicer


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    robot_pb2_grpc.add_PathFinderServicer_to_server(PathFinderServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    print("Сервер запущен на порту: 50051")
    await server.wait_for_termination()
    print("Сервер остановлен!")


if __name__ == "__main__":
    asyncio.run(serve())
