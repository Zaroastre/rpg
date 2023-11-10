import pygame
from abc import abstractmethod
from math import sqrt, atan2, cos, sin, degrees, radians
from typing import TypeVar, Generic
from datetime import datetime

_T = TypeVar("_T")
SCREEN_WIDTH: int = 1920
SCREEN_HEIGHT: int = 1080

class Optional(Generic[_T]):
    """Class that represents a object that can contains a value.
    It's usefull to not handle NullPointerException on null values.
    """
    def __init__(self, data: _T) -> None:
        self.__data: _T = data
    
    def is_present(self) -> bool:
        """Check is a value is present.

        Returns:
            bool: True or False
        """
        return self.__data is not None
    
    def is_empty(self) -> bool:
        """Check is a value is missing

        Returns:
            bool: True or False
        """
        return self.__data is None
    
    def get(self) -> _T:
        """Retrieve the value.

        Raises:
            ValueError: If the value is None

        Returns:
            _T: The value
        """
        if (self.__data is None):
            raise ValueError("NPE")
        return self.__data
        
    @staticmethod
    def of_nullable(data: _T):
        """Return a Optional that can contains an empty value.

        Args:
            data (_T): The value

        Returns:
            Optional[_T]: The optional wi the given value.
        """
        return Optional(data=data)
    
    @staticmethod
    def of(data: _T):
        """Return an optional that contains a non null value.

        Args:
            data (_T): The value

        Raises:
            ValueError: Null Pointer Exception is the value is None

        Returns:
            Optional[_T]: The value
        """
        if (data is None):
            raise ValueError("NPE")
        return Optional(data=data)
    
    @staticmethod
    def empty():
        """Return an Optional without any value.

        Returns:
            None: None value
        """
        return Optional(data=None)

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

    @staticmethod
    def compute_rotation_angle(point1: Position, point2: Position, point3: Position) -> float:
        angle = atan2(point2.y - point1.y, point2.x - point1.x) - atan2(point3.y - point1.y, point3.x - point1.x)
        angle_degrees = degrees(angle)
        return angle_degrees

    @staticmethod
    def compute_rotation_point(point: Position, rotation_center: Position, angle: float) -> Position:
        relative_x: float = point.x - rotation_center.x
        relative_y: float = point.y - rotation_center.y
        rotated_x: float = relative_x * cos(angle) - relative_y * sin(angle)
        rotated_y: float = relative_x * sin(angle) + relative_y * cos(angle)

        return Position((rotated_x + rotation_center.x), (rotated_y + rotation_center.y))

class Bone:
    def __init__(self, start: Position, end: Position, thickness: float) -> None:
        self.__start: Position = start
        self.__end: Position = end
        self.__thickness: float = thickness
        self.__parent: Optional[Bone] = Optional.empty()
        self.__children: list[Bone] = []

class Skeleton:
    def __init__(self) -> None:
        self.__bones: list[Bone] = []

class Point(pygame.sprite.Sprite, Draw,InputEventHandler):
    """_summary_

    Args:
        pygame (_type_): _description_
        Draw (_type_): _description_
    """
    UNSELECTED_COLOR: pygame.Color = pygame.Color(255,255,255)
    SELECTED_COLOR: pygame.Color = pygame.Color(255,0,0)
    TRANSPARENT: pygame.Color = pygame.Color(0,0,0,0)
    TOTAL_CREATED: int = 0
    def __init__(self, position: Position) -> None:
        pygame.sprite.Sprite.__init__(self)
        Point.TOTAL_CREATED += 1
        self.__name: str = "PNT-#"+str(Point.TOTAL_CREATED)
        self.__radius: float = 10.0
        self.__texture = pygame.Surface([self.__radius*2, self.__radius*2])
        self.parent: Point|None = None
        self.position: Position = position
        self.__is_selected: bool = False
        self.__hitbox: pygame.Rect = None
        self.__font_size: int = 20
        self.__font: pygame.font.Font = pygame.font.Font(None, self.__font_size)
        self.__font_color: pygame.Color = pygame.Color(255,255,255)
        self.__title: pygame.Surface = self.__font.render(self.name, True, self.__font_color)
        self.__children: list[Point] = []

    def get_children(self) -> list:
        return self.__children

    def is_selected(self) -> bool:
        return self.__is_selected

    @property
    def name(self) -> str:
        return self.__name

    @property
    def hitbox(self) -> pygame.Rect:
        return self.__hitbox
    
    def select(self):
        self.__is_selected = True
    
    def unselect(self):
        self.__is_selected = False

    def handle(self, event: pygame.event.Event):
        mouse_position: tuple[int, int] = pygame.mouse.get_pos()
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if (self.__hitbox.collidepoint(mouse_position)):
                print(f"POINT {self.__name} is selected")
                self.select()

    def draw(self, surface: pygame.Surface):
        self.__texture.fill(Point.TRANSPARENT)
        point_color: pygame.Color
        if (self.is_selected()):
            point_color = Point.SELECTED_COLOR
        else:
            point_color = Point.UNSELECTED_COLOR
        self.__hitbox = pygame.draw.circle(self.__texture, point_color, (self.__radius, self.__radius), self.__radius)
        self.__hitbox = surface.blit(self.__texture, (self.position.x-self.__radius,self.position.y-self.__radius))
        surface.blit(self.__title, (self.position.x+self.__radius*2,self.position.y-(self.__radius/2)))

    def copy(self):
        copy: Point = Point(Position(self.position.x, self.position.y, self.position.z))
        return copy

    def __repr__(self) -> str:
        return f"{self.__name}(P={self.parent})"

class Frame(Draw):
    def __init__(self, skeleton: Skeleton) -> None:
        self.__skeleton: Skeleton = skeleton
        self.__points: list[Point] = []
        self.__is_selected: bool = False

    @property
    def skeleton(self) -> Skeleton:
        return self.__skeleton
    
    @property
    def is_selected(self) -> bool:
        return self.__is_selected

    def get_points(self) -> list[Point]:
        return self.__points.copy()

    def add_point(self, point: Point):
        self.__points.append(point)
        
    def delete_point(self, point: Point):
        self.__points.remove(point)

    def delete_all_points(self):
        self.__points.clear()

    def select(self):
        self.__is_selected = True
    def unselect(self):
        self.__is_selected = False

    def copy(self):
        copies_associations: dict = {}
        dupliacted_frame: Frame = Frame(skeleton=None)
        for point in self.get_points():
            duplicated_point: Point = point.copy()
            copies_associations[point.name] = duplicated_point.name
            dupliacted_frame.add_point(duplicated_point)
        for point in self.get_points():
            if (point.parent is not None):
                dupliacted_point_name: str = copies_associations.get(point.name)
                dupliacted_parent_point_name: str = copies_associations.get(point.parent.name)
                copied_points_with_name: list[Point] = [duplicated_point for duplicated_point in dupliacted_frame.get_points() if duplicated_point.name == dupliacted_point_name]
                copied_parent_points_with_name: list[Point] = [duplicated_point for duplicated_point in dupliacted_frame.get_points() if duplicated_point.name == dupliacted_parent_point_name]
                if (len(copied_points_with_name) > 0 and len(copied_parent_points_with_name) > 0):
                    copied_points_with_name[0].parent = copied_parent_points_with_name[0]
                
        return dupliacted_frame

    def __draw_points(self, surface: pygame.Surface):
        for point_to_draw in self.get_points():
            point_to_draw.draw(surface)

    def __draw_line_between_each_points(self, surface: pygame.Surface):
        if (len(self.get_points()) > 1):
            for point in self.get_points():
                if (point.parent is not None):
                    parent: Point = point.parent
                    pygame.draw.line(surface, pygame.Color(255,255,255), (parent.position.x, parent.position.y), (point.position.x, point.position.y))

    def draw(self, master: pygame.Surface):
        self.__draw_points(master)
        self.__draw_line_between_each_points(master)

class Timeline(pygame.sprite.Sprite, Draw, InputEventHandler):
    
    FRAME_MARGIN: int = 5
    def __init__(self, width: float, height: float, position: Position) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.__frames: list[Frame] = []
        self.texture = pygame.Surface([width, height])
        self.position: Position = position
        self.background_color: pygame.Color = pygame.Color(50, 50, 50)
        self.selected_frame: Optional[Frame] = Optional.empty()
        
        self.frame_texture: pygame.Surface = pygame.Surface((self.texture.get_height()-(Timeline.FRAME_MARGIN*2), self.texture.get_height()-(Timeline.FRAME_MARGIN*2)))
        self.frame_background_color: pygame.Color = pygame.Color(150,150,150)
        self.frame_texture_background_color: pygame.Color = pygame.Color(255,0,0)
        self.__on_selected_frame_change_callback = None
        
        self.font_size: int = 24
        self.font: pygame.font.Font = pygame.font.Font(None, self.font_size)
        self.font_color: pygame.Color = pygame.Color(255,255,255)
        self.title: pygame.Surface = self.font.render("Timeline", True, self.font_color)
    
    def get_frames(self) -> list[Frame]:
        return self.__frames.copy()
    
    def add_event_listener_on_selected_frame_change(self, callback):
        self.__on_selected_frame_change_callback = callback
    
    def add_frame(self, frame_to_add: Frame):
        self.__frames.append(frame_to_add)
    
    def select_frame(self, frame_to_select: Frame):
        print("Select FRAME")
        if (frame_to_select in self.get_frames()):
            for frame in self.get_frames():
                frame.unselect()
            frame_to_select.select()
            self.selected_frame = Optional.of_nullable(frame_to_select)
            if (self.__on_selected_frame_change_callback is not None):
                self.__on_selected_frame_change_callback(frame_to_select)
    
    def delete_frame(self, frame_to_delete: Frame):
        if (frame_to_delete in self.__frames):
            self.__frames.remove(frame_to_delete)
    
    def select_previous_frame(self):
        index: int = self.__frames.index(self.selected_frame.get())
        if (index > 0):
            self.select_frame(self.__frames[index-1])
            
    def select_next_frame(self):
        index: int = self.__frames.index(self.selected_frame.get())
        if (index < (len(self.__frames)-1)):
            self.select_frame(self.__frames[index+1])
    
    def __handle_duplicate_frame(self):
        print("Duplicate FRAME")
        if (self.selected_frame.is_present()):
            frame: Frame = self.selected_frame.get()
            new_frame: Frame = frame.copy()
            self.__frames.append(new_frame)
            self.select_frame(new_frame)

    def __handle_delete_frame(self):
        print("Delete FRAME")
        if (self.selected_frame.is_present()):
            frame_to_delete: Frame = self.selected_frame.get()
            index: int = self.__frames.index(frame_to_delete)
            if (index >= 0):
                self.delete_frame(frame_to_delete)
            self.selected_frame = Optional.empty()
            if (index == 0):
                if (len(self.__frames) > 0):
                    self.select_frame(self.__frames[0])
            elif (index > 0):
                self.select_frame(self.__frames[index-1])
            if (self.selected_frame.is_empty()):
                frame: Frame = Frame(skeleton=None)
                self.__frames.append(frame)
                self.select_frame(frame)

    def __handle_select_previous_frame(self):
        print("Select PREVIOUS FRAME")
        if (self.selected_frame.is_present()):
            self.select_previous_frame()
            
    
    def __handle_select_next_frame(self):
        print("Select NEXT FRAME")
        if (self.selected_frame.is_present()):
            self.select_next_frame()
            

    def handle(self, event: pygame.event.Event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_c):
            self.__handle_duplicate_frame()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_d):
            self.__handle_delete_frame()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
            self.__handle_select_previous_frame()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
            self.__handle_select_next_frame()

    def draw(self, master: pygame.Surface):
        # Timeline
        self.texture.fill(self.background_color)
        
        # Frame
        self.frame_texture.fill(self.frame_background_color)
        frame_position_x: int = Timeline.FRAME_MARGIN
        
        for frame in self.__frames:
            if (frame.is_selected):
                self.frame_texture.fill(self.frame_texture_background_color)
            else:
                self.frame_texture.fill(self.frame_background_color)
            self.texture.blit(self.frame_texture, (frame_position_x, Timeline.FRAME_MARGIN))
            frame_position_x += (self.frame_texture.get_width()+(Timeline.FRAME_MARGIN*2))

        self.texture.blit(self.title, (0, 0))
        master.blit(self.texture, (self.position.x, self.position.y))

class Video(Draw, InputEventHandler):
    def __init__(self, fps: int, width: float, height: float, position: Position) -> None:
        self.frames: list[Frame] = []
        self.texture: pygame.Surface = pygame.Surface([width, height])
        self.position: Position = position
        self.frames_per_seconds: int = fps
        self.frame_index: int = 0
        self.frame_display_duration: float = 1_000 / self.frames_per_seconds
        self.last_render_timestamp: int = 0
        self.font_size: int = 24
        self.font: pygame.font.Font = pygame.font.Font(None, self.font_size)
        self.font_color: pygame.Color = pygame.Color(255,255,255)
        self.title: pygame.Surface = self.font.render("Video", True, self.font_color)

    def set_movie(self, movie: list[Frame]):
        self.frames = movie

    def draw(self, master: pygame.Surface):
        self.texture.fill(pygame.Color(0,0,0))
        now: int = int(datetime.now().timestamp()*1000)
        if ((self.last_render_timestamp + self.frame_display_duration) < now):
            self.frame_index += 1
            if (self.frame_index >= len(self.frames)):
                self.frame_index = 0
            self.last_render_timestamp = now
        try:
            self.frames[self.frame_index].draw(self.texture)
        except IndexError:
            print(f"Array Size: {len(self.frames)}, requested index: {self.frame_index}")
        self.texture.blit(self.title, (0,0))
        master.blit(self.texture, (self.position.x, self.position.y))
    
    def handle(self, event: pygame.event.Event):
        pass

class Workspace(pygame.sprite.Sprite, Draw, InputEventHandler):
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
        self.title_font_size: int = 24
        self.title_font: pygame.font.Font = pygame.font.Font(None, self.title_font_size)
        self.title_font_color: pygame.Color = pygame.Color(255,255,255)
        self.title: pygame.Surface = self.title_font.render("Workspace", True, self.title_font_color)
        
        self.mouse_font_size: int = 20
        self.mouse_font: pygame.font.Font = pygame.font.Font(None, self.mouse_font_size)
        self.mouse_font_color: pygame.Color = pygame.Color(255,255,255)
        self.mouse_label: pygame.Surface = self.mouse_font.render("Workspace", True, self.mouse_font_color)
        
        self.mouse_position: Position = Position(0, 0)

    def __draw_points(self, master: pygame.Surface):
        for point in self.frame.get_points():
            point.draw(master)

    def __draw_line_between_each_points(self, master: pygame.Surface):
        if (len(self.frame.get_points()) > 1):
            for point in self.frame.get_points():
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
        self.texture.fill(pygame.Color(30, 30, 30))
        
        # Draw all points
        self.__draw_points(self.texture)
        
        # Draw a line between each points.
        self.__draw_line_between_each_points(self.texture)

        # Draw the direction motion line.
        self.__draw_direction_motion_line(self.texture)

        # Draw the direction motion circle.
        self.__draw_direction_motion_circle(self.texture)
        
        self.texture.blit(self.title, (0, 0))
        self.texture.blit(self.mouse_font.render(f"Mouse: (x:{self.mouse_position.x}, y:{self.mouse_position.y})", True, self.mouse_font_color), (0, self.height-self.mouse_font_size))
        master.blit(self.texture, (self.position.x, self.position.y))

    def __handle_clear_scene(self):
        print("Delete all POINTS")
        self.frame.delete_all_points()
        self.selected_point = Optional.empty()
    
    def __retrieve_children(self, parent: Point) -> list[Point]:
        print(f"Retrieve list of childre for POINT {parent.name}")
        children: list[Point] = [point for point in self.frame.get_points() if point.parent == parent]
        for child in children:
            depth_children: list[Point] = self.__retrieve_children(child)
            for depth_child in depth_children:
                children.append(depth_child)
        children = list(set(children))
        print("Children are: " + str(children))
        return list(set(children))
    
    def __delete_point(self, point_to_delete: Point, must_delete_tree: bool = True):
        print(f"Delete POINT {point_to_delete.name}")
        try:
            self.frame.delete_point(point_to_delete)
        except:
            pass
        if (must_delete_tree):
            for other_point in self.__retrieve_children(point_to_delete):
                if (other_point.parent == point_to_delete):
                    print(f"Delete orphan POINT {other_point.name}")
                    self.__delete_point(other_point)

    def __handle_delete_selected_point(self):
        print("Must delete POINT")
        if (self.selected_point.is_present()):
            point: Point = self.selected_point.get()
            print(f"POINT ({point.name}) will be deleted")
            self.__delete_point(point)
            if (point.parent is not None):
                point.parent.select()
                self.selected_point = Optional.of_nullable(point.parent)
            
    def __handle_move_point_to_pointer_position(self):
        print("Must move POINT to Mouse's Position")
        if (self.selected_point.is_present()):
            point: Point = self.selected_point.get()
            print(f"POINT ({point.name}) must move to (x={self.mouse_position.x}, y={self.mouse_position.y}) ")
            point.position = self.mouse_position

    def __handle_move_point_on_circle(self):
        print("Must move POINT on CIRCLE.")
        if (self.selected_point.is_present()):
            point: Point = self.selected_point.get()
            print(f"POINT to move: {point.name}")
            if (point.parent is not None):
                parent: Point = point.parent
                angle = atan2(self.mouse_position.y - parent.position.y, self.mouse_position.x - parent.position.x)
                radius: float = sqrt((parent.position.x - point.position.x)**2 + (parent.position.y - point.position.y)**2)
                point_x = parent.position.x + radius * cos(angle)
                point_y = parent.position.y + radius * sin(angle)
                point_old_position: Position = point.position
                point.position = Position(point_x, point_y)
                children_points: list[Point] = self.__retrieve_children(point)
                rotate_angle: float = -Geometry.compute_rotation_angle(parent.position, point_old_position, point.position)
                for child in children_points:
                    child.position = Geometry.compute_rotation_point(child.position, parent.position, radians(rotate_angle))
                    

    def __handle_move_point_on_line(self):
        print("Must move POINT on LINE.")
        if (self.selected_point.is_present()):
            point: Point = self.selected_point.get()
            print(f"POINT to move: {point.name}")
            if (point.parent is not None):
                parent: Point = point.parent
                distance_x = self.texture.get_width() - 0
                distance_y = self.texture.get_height() - 0
                line_length = (distance_x ** 2 + distance_y ** 2) ** 0.5
                if line_length > 0:
                    t = ((self.mouse_position.x - 0) * distance_x + (self.mouse_position.y - 0) * distance_y) / (line_length ** 2)
                    t = max(0, min(1, t))
                    point_x = 0 + t * distance_x
                    point_y = 0 + t * distance_y
                point_x = int(parent.position.x + t * (point.position.x - parent.position.x))
                point_y = int(parent.position.y + t * (point.position.y - parent.position.y))
                point.position = Position(point_x, point_y)

    def handle_create_new_point(self):
        pass
    
    def get_selected_point_with_mouse(self) -> Optional[Point]:
        selected_point_with_mouse: Optional[Point] = Optional.empty()
        selected_points_with_mouse: list[Point] = [point for point in self.frame.get_points() if point.hitbox.collidepoint((self.mouse_position.x, self.mouse_position.y))]
        if (len(selected_points_with_mouse) > 0):
            selected_point_with_mouse = Optional.of_nullable(selected_points_with_mouse[0])
        return selected_point_with_mouse

    def __handle_select_point(self, point: Point):
        for other_point in self.frame.get_points():
            other_point.unselect()
        point.select()
        self.selected_point = Optional.of(point)

    def __handle_create_new_point(self):
        selected_points: list[Point] = [point for point in self.frame.get_points() if point.is_selected()]
        for point in self.frame.get_points():
            point.unselect()
        new_point: Point = Point(Position(self.mouse_position.x, self.mouse_position.y))
        new_point.select()
        self.selected_point = Optional.of(new_point)
        if (len(selected_points) > 0):
            new_point.parent = selected_points[0]
        self.frame.add_point(new_point)

    def handle(self, event: pygame.event.Event):
        cursor_position: tuple[int] = pygame.mouse.get_pos()
        self.mouse_position = Position(cursor_position[0], cursor_position[1])
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.__handle_clear_scene()
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE):
            self.__handle_delete_selected_point()
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
            print("Must deplay Radius Circle")
            self.must_display_circle = True
        elif (event.type == pygame.KEYUP and event.key == pygame.K_r):
            print("Must hide Radius Circle")
            self.must_display_circle = False
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_l):
            print("Must deplay Line")
            self.must_display_line = True
        elif (event.type == pygame.KEYUP and event.key == pygame.K_l):
            print("Must hide Line")
            self.must_display_line = False
        else:
            if (self.hitbox.collidepoint((self.mouse_position.x, self.mouse_position.y))):
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    print("Mouse clicked in Workspace Area")
                    self.is_dragging = True
                    selected_points_with_mouse: Optional[Point] = self.get_selected_point_with_mouse()
                    if (selected_points_with_mouse.is_present()):
                        selected_point_with_mouse: Point = selected_points_with_mouse.get()
                        self.__handle_select_point(selected_point_with_mouse)
                    else:
                        self.__handle_create_new_point()
                if (event.type == pygame.MOUSEBUTTONUP):
                    self.is_dragging = False
                if (event.type == pygame.MOUSEMOTION):
                    if (self.is_dragging):
                        self.__handle_move_point_to_pointer_position()
                    if (self.must_display_circle):
                        self.__handle_move_point_on_circle()
                    if (self.must_display_line):
                        self.__handle_move_point_on_line()

class App:
    """Class that represents the program.
    """
    FRAMES_PER_SECOND: int = 60
    WINDOW_WIDTH: int = SCREEN_WIDTH
    WINDOW_HEIGHT: int = SCREEN_HEIGHT
    TIMELINE_WIDTH: int = WINDOW_WIDTH
    TIMELINE_HEIGHT: int = 100
    WORKSPACE_WIDTH: int = WINDOW_WIDTH / 2
    WORKSPACE_HEIGHT: int = WINDOW_HEIGHT - TIMELINE_HEIGHT
    MOVIE_WIDTH: int = WORKSPACE_WIDTH
    MOVIE_HEIGHT: int = WORKSPACE_HEIGHT
    MOVIE_FPS: int = 30
    BACKGROUND_COLOR: pygame.Color = pygame.Color(0,0,0)
    
    def __init__(self) -> None:
        print("Starting application...")
        pygame.init()
        print("Creating window...")
        # self.screen: pygame.Surface = pygame.display.set_mode((App.WINDOW_WIDTH, App.WINDOW_HEIGHT))
        self.screen: pygame.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Sprites Motion Creator")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.is_running: bool = True
        
        print("Creating default frame")
        skeleton: Skeleton = Skeleton()
        frame: Frame = Frame(skeleton=skeleton)
        frame.select()
        print("Creating Workspace")
        self.workspace: Workspace = Workspace(App.WORKSPACE_WIDTH, App.WORKSPACE_HEIGHT, Position(0, 0))
        self.workspace.frame = frame
        print("Creating Video")
        self.video: Video = Video(App.MOVIE_FPS, App.MOVIE_WIDTH, App.MOVIE_HEIGHT, Position(App.MOVIE_WIDTH, 0))
        self.video.frames.append(frame)
        print("Creating Timeline")
        self.timeline: Timeline = Timeline(App.TIMELINE_WIDTH, App.TIMELINE_HEIGHT, Position(0, App.WINDOW_HEIGHT-App.TIMELINE_HEIGHT))
        self.timeline.add_frame(frame)
        self.timeline.select_frame(frame)
        self.timeline.add_event_listener_on_selected_frame_change(self.on_selected_frame_change_handler)
    
    def on_selected_frame_change_handler(self, selected_frame: Frame):
        print("Selected frame has changed.")
        self.workspace.frame = selected_frame
    
    def run(self):
        while (self.is_running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                else:
                    # HANDLE YOUR GAME HERE
                    self.workspace.handle(event)
                    self.timeline.handle(event)
                    self.video.handle(event)
                    self.video.set_movie(self.timeline.get_frames())

            self.screen.fill(App.BACKGROUND_COLOR)

            # RENDER YOUR GAME HERE
            self.workspace.draw(self.screen)
            self.timeline.draw(self.screen)
            self.video.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(App.FRAMES_PER_SECOND)
        pygame.quit()

    @staticmethod
    def main():
        app: App = App()
        app.run()

if (__name__ == "__main__"):
    App.main()