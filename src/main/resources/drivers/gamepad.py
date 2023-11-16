from argparse import ArgumentParser, Namespace
from sys import exit as shutdown
from socket import socket as Socket, AF_INET, SOCK_DGRAM
import pygame

class JGamePadServer:
    
    def __init__(self, port: int) -> None:
        self.__port: int = port
        self.__host: str = "127.0.0.1"
    
    def start(self):
        
        # udp_client: Socket = Socket(AF_INET, SOCK_DGRAM)
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        is_connected: bool = True
        joystick_events = [
            pygame.JOYAXISMOTION,
            pygame.JOYBALLMOTION,
            pygame.JOYBUTTONDOWN,
            pygame.JOYBUTTONUP,
            pygame.JOYHATMOTION
        ]
        while (is_connected):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_connected = False
                elif event.type in joystick_events:
                    udp_client: Socket = Socket(AF_INET, SOCK_DGRAM)
                    try:
                        udp_client.sendto(str(event).encode(), (self.__host, self.__port))
                    except Exception as exception:
                        raise exception
                    finally:
                        # Fermez le socket client
                        udp_client.close()

    
    @staticmethod
    def main():
        pygame.init()
        pygame.joystick.init()
        parser: ArgumentParser = ArgumentParser(description="Gamepad Driver")
        parser.add_argument('--port', type=int, help="Local UDP port ")

        command_line_arguments: Namespace = parser.parse_args()

        if (command_line_arguments.port is not None):
            port: int = command_line_arguments.port
            server: JGamePadServer = JGamePadServer(port=port)
            server.start()
        else:
            shutdown(-1)

if (__name__ == "__main__"):
    JGamePadServer.main()