import pygame
from abc import abstractmethod
from math import sqrt, atan2, cos, sin
from typing import TypeVar, Generic

_T = TypeVar("_T")

class InputEventHandler:
    """Interface that represents an events handler throw by user.
    """
    @abstractmethod
    def handle(self, event: pygame.event.Event):
        """Handle the given event.

        Args:
            event (pygame.event.Event): The user input event.
        """
        raise NotImplementedError()

class Draw:
    """Interface that represents a drawable object.
    """
    @abstractmethod
    def draw(self, master: pygame.Surface):
        """Draw something on the master surface.

        Args:
            master (pygame.Surface): The master surface that must be painted.
        """
        raise NotImplementedError()

class Position:
    """Class that represents a position in a geomatric space.
    """
    def __init__(self, x: float, y: float, z: float = 0.0) -> None:
        """Default constructor.

        Args:
            x (float): X
            y (float): Y
            z (float, optional): Z. Defaults to 0.0.
        """
        self.x: float = x
        self.y: float = y
        self.z: float = z
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

class Geometry:
    """Utilitary class that can be used to computes usefull algorythm for geometry computation.
    """
    
    @staticmethod
    def compute_slope(point1: Position, point2: Position) -> float:
        delta_y = point2.y - point1.y
        delta_x = point2.x - point1.x
        print(f"POINT: {point1}-{point2}=({delta_x}, {delta_y})")
        print(f"{delta_y} / {delta_x}")
        return delta_y / delta_x
    
    @staticmethod
    def compute_origin_point(point1: Position, point2: Position) -> Position:
        """Compute the original point from the two given points.

        Args:
            point1 (Position): First point
            point2 (Position): Second point

        Returns:
            Position: The new computed position
        """
        SLOPE: float = Geometry.compute_slope(point1, point2)
        COEFFICIENT = -1
        COEFFICIENT_OF_LINE = -SLOPE * point1.x - COEFFICIENT * point1.y
        X = COEFFICIENT_OF_LINE / SLOPE
        Y = 0
        return Position(X, Y)

    @staticmethod
    def calculate_point_from_y(point1: Position, point2: Position, y: float) -> Position:
        """Compute new point using 2 existing points and knowing the Y position.

        Args:
            point1 (Position): Firsrt point
            point2 (Position): Second point
            y (float): Y position of the new position to compute

        Returns:
            Position: The computed position
        """
        # Vérifier si les points sont sur la même ligne horizontale
        if point1.y == point2.y and point1.y != y:
            raise ValueError("Les points ne forment pas une ligne horizontale à la hauteur de Y.")
        x: float = 0.0
        if point1.y == point2.y:
            x = (point1.x + point2.x) / 2
        else:
            x = point1.x + (y - point1.y) * (point2.x - point1.x) / (point2.y - point1.y)
        return Position(x, y)

    @staticmethod
    def compute_new_point_using_x(point1: Position, point2: Position, x: float) -> Position:
        """Compute new point using 2 exisitng points and knowing x position of the new position to compute.

        Args:
            point1 (Position): First point
            point2 (Position): Second point
            x (int): X of the new position

        Returns:
            Position: The new computed position
        """
        SLOPE = Geometry.compute_slope(point1, point2)
        Y = SLOPE * (x - point1.x) + point1.y
        return Position(x, Y)

class Optional(Generic[_T]):
    def __init__(self, data: _T) -> None:
        self.data: _T = data
    
    def is_present(self) -> bool:
        return self.data is not None
    
    def is_empty(self) -> bool:
        return self.data is None
    
    def get(self) -> _T:
        if (self.data is None):
            raise ValueError("NPE")
        return self.data
        
    @staticmethod
    def of_nullable(data: _T):
        return Optional(data=data)
    
    @staticmethod
    def empty():
        return Optional(data=None)

class Point(pygame.sprite.Sprite, Draw,InputEventHandler):
    """_summary_

    Args:
        pygame (_type_): _description_
        Draw (_type_): _description_
    """
    UNSELECTED_COLOR: pygame.Color = pygame.Color(255,255,255)
    SELECTED_COLOR: pygame.Color = pygame.Color(255,0,0)
    TOTAL_CREATED: int = 0
    def __init__(self, position: Position) -> None:
        pygame.sprite.Sprite.__init__(self)
        Point.TOTAL_CREATED += 1
        self.name: str = "PNT-#"+str(Point.TOTAL_CREATED)
        self.radius: float = 10.0
        self.texture = pygame.Surface([self.radius, self.radius])
        self.parent: Point|None = None
        self.position: Position = position
        self.is_selected: bool = False
        self.hitbox: pygame.Rect = None


    def handle(self, event: pygame.event.Event):
        mouse_position = pygame.mouse.get_pos()
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (self.hitbox.collidepoint(mouse_position)):
                self.is_selected = True

    def draw(self, master: pygame.Surface):
        if (self.is_selected):
            self.hitbox = pygame.draw.circle(master, Point.SELECTED_COLOR, (self.position.x,self.position.y), self.radius)
        else:
            self.hitbox = pygame.draw.circle(master, Point.UNSELECTED_COLOR, (self.position.x,self.position.y), self.radius)

    def __repr__(self) -> str:
        return f"{self.name}(P={self.parent})"

class Frame(Draw, InputEventHandler):
    def __init__(self) -> None:
        self.points: list[Point] = []
        self.is_selected: bool = False

class Timeline(pygame.sprite.Sprite, Draw, InputEventHandler):
    FRAME_MARGIN: int = 5
    def __init__(self, width: float, height: float, position: Position) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.frames: list[Frame] = []
        self.texture = pygame.Surface([width, height])
        self.position: Position = position
        self.background_color: pygame.Color = pygame.Color(50, 50, 50)
        
        self.frame_texture: pygame.Surface = pygame.Surface((self.texture.get_height()-(Timeline.FRAME_MARGIN*2), self.texture.get_height()-(Timeline.FRAME_MARGIN*2)))
        self.frame_background_color: pygame.Color = pygame.Color(150,150,150)
    
    def handle(self, event: pygame.event.Event):
        pass
    
    def draw(self, master: pygame.Surface):
        # Timeline
        self.texture.fill(self.background_color)
        master.blit(self.texture, (self.position.x, self.position.y))
        
        # Frame
        self.frame_texture.fill(self.frame_background_color)
        frame_position_x: int = self.position.x + Timeline.FRAME_MARGIN
        
        for frame in self.frames:
            if (frame.is_selected):
                self.frame_texture.copy()
                frame_texture_for_selected_frame = self.frame_texture.copy()
                frame_texture_for_selected_frame.fill(pygame.Color(200,0,0))
                master.blit(frame_texture_for_selected_frame, (frame_position_x, self.position.y + Timeline.FRAME_MARGIN))
            else:
                master.blit(self.frame_texture, (frame_position_x, self.position.y + Timeline.FRAME_MARGIN))
                
            frame_position_x += (self.frame_texture.get_width()+(Timeline.FRAME_MARGIN*2))
    

class Video(Draw, InputEventHandler):
    def __init__(self) -> None:
        self.frames: list[Frame] = []

    def draw(self, master: pygame.Surface):
        pass
    
    def handle(self, event: pygame.event.Event):
        pass

class WorkspaceBuilder(pygame.sprite.Sprite, Draw, InputEventHandler):
    def __init__(self, width: float, height: float, position: Position) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.frame: Frame|None = None
        self.texture: pygame.Surface = pygame.Surface([width, height])
        self.width: float = width
        self.height: float = height
        self.position: Position = position
        self.hitbox: pygame.Rect = self.texture.fill(pygame.Color(30, 30, 30))
        self.must_display_circle: bool = False
        self.must_display_line: bool = False
        self.is_dragging: bool = False
        self.selected_point: Optional[Point] = Optional.empty()

    # def get_selected_point(self) -> Point|None:
    #     point: Point|None = None
    #     selected_points: list[Point] = [point for point in self.frame.points if point.is_selected]
    #     if (len(selected_points >= 1)):
    #         point = selected_points[0]
    #     return point

    def __draw_points(self, master: pygame.Surface):
        for point in self.frame.points:
            point.draw(master)

    def __draw_line_between_each_points(self, master: pygame.Surface):
        if (len(self.frame.points) > 1):
            for point in self.frame.points:
                if (point.parent is not None):
                    parent: Point = point.parent
                    pygame.draw.line(master, pygame.Color(255,255,255), (parent.position.x, parent.position.y), (point.position.x, point.position.y))

    def __draw_direction_motion_line(self, master: pygame.Surface):
        if (self.must_display_line):
            if (self.selected_point.is_present()):
                point: Point = self.selected_point.get()
                parent: Point = point.parent
                if (parent is not None):
                    origin: Position = Geometry.compute_origin_point(parent.position, point.position)
                    end: Position = Geometry.compute_new_point_using_x(origin, point.position, self.texture.get_width())
                    pygame.draw.line(master, pygame.Color(0,255,0), (origin.x, origin.y), (end.x, end.y))

    def __draw_direction_motion_circle(self, master: pygame.Surface):
        if (self.must_display_circle):
            if (self.selected_point.is_present()):
                point: Point = self.selected_point.get()
                parent: Point = point.parent
                if (parent is not None):
                    radius: float = sqrt((parent.position.x - point.position.x)**2 + (parent.position.y - point.position.y)**2)
                    pygame.draw.circle(master, pygame.Color(0,255,0), (parent.position.x, parent.position.y), radius, 1)
        

    def draw(self, master: pygame.Surface):
        master.blit(self.texture, (self.position.x, self.position.y))
        
        # Draw all points
        self.__draw_points(master)
        
        # Draw a line between each points.
        self.__draw_line_between_each_points(master)

        # Draw the direction motion line.
        self.__draw_direction_motion_line(master)

        # Draw the direction motion circle.
        self.__draw_direction_motion_circle(master)

    def __handle_clear_scene(self):
        self.frame.points.clear()
        self.selected_point = Optional.empty()
    
    def __retrieve_children(self, parent: Point) -> list[Point]:
        children: list[Point] = [point for point in self.frame.points if point.parent == parent]
        for child in children:
            depth_children: list[Point] = self.__retrieve_children(child)
            for depth_child in depth_children:
                children.append(depth_child)
        return list(set(children))
    
    def __delete_point(self, point_to_delete: Point, must_delete_tree: bool = True):
        try:
            self.frame.points.remove(point_to_delete)
        except:
            pass
        if (must_delete_tree):
            for other_point in self.__retrieve_children(point_to_delete):
                if (other_point.parent == point_to_delete):
                    self.__delete_point(other_point)
            
    
    def __handle_delete_selected_point(self):
        print("Start deletion...")
        for point in self.frame.points:
            print(point)
        if (self.selected_point.is_present()):
            point: Point = self.selected_point.get()
            self.__delete_point(point)
            if (point.parent is not None):
                point.parent.is_selected = True
                self.selected_point = Optional.of_nullable(point.parent)
        print("Deletion terminated.")
        for point in self.frame.points:
            print(point)
            
    def __handle_move_point_to_pointer_position(self, new_position: Position):
        if (self.selected_point.is_present()):
            point: Point = self.selected_point.get()
            point.position = new_position

    def __handle_move_point_on_circle(self, mouse_position: Position):
        if (self.selected_point.is_present()):
            point: Point = self.selected_point.get()
            if (point.parent is not None):
                parent: Point = point.parent
                angle = atan2(mouse_position.y - parent.position.y, mouse_position.x - parent.position.x)
                radius: float = sqrt((parent.position.x - point.position.x)**2 + (parent.position.y - point.position.y)**2)
                point_x = parent.position.x + radius * cos(angle)
                point_y = parent.position.y + radius * sin(angle)
                point.position = Position(point_x, point_y)

    def __handle_move_point_on_line(self, mouse_position: Position):
        if (self.selected_point.is_present()):
            point: Point = self.selected_point.get()
            if (point.parent is not None):
                parent: Point = point.parent
                distance_x = self.texture.get_width() - 0
                distance_y = self.texture.get_height() - 0
                line_length = (distance_x ** 2 + distance_y ** 2) ** 0.5
                if line_length > 0:
                    t = ((mouse_position.x - 0) * distance_x + (mouse_position.y - 0) * distance_y) / (line_length ** 2)
                    t = max(0, min(1, t))
                    point_x = 0 + t * distance_x
                    point_y = 0 + t * distance_y
                point_x = int(parent.position.x + t * (point.position.x - parent.position.x))
                point_y = int(parent.position.y + t * (point.position.y - parent.position.y))
                point.position = Position(point_x, point_y)

    def handle(self, event: pygame.event.Event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.__handle_clear_scene()
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE):
            self.__handle_delete_selected_point()
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_LALT):
            self.must_display_circle = True
        elif (event.type == pygame.KEYUP and event.key == pygame.K_LALT):
            self.must_display_circle = False
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT):
            self.must_display_line = True
        elif (event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT):
            self.must_display_line = False
        else:
            mouse_position = pygame.mouse.get_pos()
            if (self.hitbox.collidepoint(mouse_position)):
                selected_point_with_mouse: Point|None = None
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    self.is_dragging = True
                    selected_points_with_mouse: list[Point] = [point for point in self.frame.points if point.hitbox.collidepoint(mouse_position)]
                    if (len(selected_points_with_mouse) > 0):
                        selected_point_with_mouse = selected_points_with_mouse[0]
                        selected_point_with_mouse.is_selected = True
                        self.selected_point = Optional.of_nullable(selected_point_with_mouse)
                    else:
                        selected_points: list[Point] = [point for point in self.frame.points if point.is_selected]
                        for point in self.frame.points:
                            point.is_selected = False
                        new_point: Point = Point(Position(mouse_position[0],mouse_position[1]))
                        new_point.is_selected = True
                        self.selected_point = Optional.of_nullable(new_point)
                        if (len(selected_points) > 0):
                            new_point.parent = selected_points[0]
                        self.frame.points.append(new_point)
                        print(new_point)
                if (event.type == pygame.MOUSEBUTTONUP):
                    self.is_dragging = False
                if (event.type == pygame.MOUSEMOTION):
                    if (self.is_dragging):
                        self.__handle_move_point_to_pointer_position(Position(mouse_position[0], mouse_position[1]))
                    if (self.must_display_circle):
                        self.__handle_move_point_on_circle(Position(mouse_position[0], mouse_position[1]))
                    if (self.must_display_line):
                        self.__handle_move_point_on_line(Position(mouse_position[0], mouse_position[1]))
class App:
    """Class that represents the program.
    """
    FRAMES_PER_SECOND: int = 60
    WINDOW_WIDTH: int = 1280
    WINDOW_HEIGHT: int = 720
    TIMELINE_WIDTH: int = WINDOW_WIDTH
    TIMELINE_HEIGHT: int = 100
    WORKSPACE_WIDTH: int = WINDOW_WIDTH / 2
    WORKSPACE_HEIGHT: int = WINDOW_HEIGHT - TIMELINE_HEIGHT
    BACKGROUND_COLOR: pygame.Color = pygame.Color(0,0,0)
 
    @staticmethod
    def main():
        
        pygame.init()
        
        screen: pygame.Surface = pygame.display.set_mode((App.WINDOW_WIDTH, App.WINDOW_HEIGHT))
        pygame.display.set_caption("Sprites Motion Creator")
        clock: pygame.time.Clock = pygame.time.Clock()
        is_running: bool = True
        
        frame: Frame = Frame()
        frame.is_selected = True
        workspace: WorkspaceBuilder = WorkspaceBuilder(App.WORKSPACE_WIDTH, App.WORKSPACE_HEIGHT, Position(0, 0))
        workspace.frame = frame
        video: Video = Video()
        video.frames.append(frame)
        timeline: Timeline = Timeline(App.TIMELINE_WIDTH, App.TIMELINE_HEIGHT, Position(0, App.WINDOW_HEIGHT-App.TIMELINE_HEIGHT))
        timeline.frames.append(frame)
        
        while (is_running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                else:
                    # HANDLE YOUR GAME HERE
                    workspace.handle(event)
                    timeline.handle(event)
                    video.handle(event)

            screen.fill(App.BACKGROUND_COLOR)

            # RENDER YOUR GAME HERE
            workspace.draw(screen)
            timeline.draw(screen)
            video.draw(screen)

            pygame.display.flip()
            clock.tick(App.FRAMES_PER_SECOND)
        pygame.quit()

if (__name__ == "__main__"):
    App.main()