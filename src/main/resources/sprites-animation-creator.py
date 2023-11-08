import pygame
from math import sqrt

class EventHandler:
    def handle(self, event: pygame.event.Event):
        pass

class Draw:
    def draw(self, master: pygame.Surface):
        pass

class Position:
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
    
    def __repr__(self) -> str:
        return "({},{})".format(self.x, self.y)

class Math:
    @staticmethod
    def find_origin_point(point1: Position, point2: Position):
    
        # Calcul de la pente (m)
        m = (point2.y - point1.y) / (point2.x - point1.x)
        
        # Coefficients de l'équation de la droite
        A = m
        B = -1
        
        # Calcul de C en utilisant l'un des points (ici, nous utilisons le premier point)
        C = -A * point1.x - B * point1.y
        
        # Calcul du point d'origine en utilisant x comme variable dépendante
        x = C / A
        y = 0
        
        return Position(x, y)

    @staticmethod
    def compute_new_point_using_x(point1: Position, point2: Position, x: int):
        # Calcul de la pente (m) de la droite
        m = (point2.y - point1.y) / (point2.x - point1.x)
        
        # Utilisation de l'équation de la droite pour calculer Y_new
        y = m * (x - point1.x) + point1.y
        
        return Position(x, y)

class Point(pygame.sprite.Sprite, Draw):
    UNSELECTED_COLOR: pygame.Color = pygame.Color(255,255,255)
    SELECTED_COLOR: pygame.Color = pygame.Color(255,0,0)
    def __init__(self, position: Position) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.radius: float = 10.0
        self.image = pygame.Surface([self.radius, self.radius])
        self.parent: Point|None = None
        self.position: Position = position
        self.is_selected: bool = False
        self.hitbox: pygame.Rect = None


    def handle(self, event: pygame.event.Event):
        
        mouse_position = pygame.mouse.get_pos()
        if (self.hitbox.collidepoint(mouse_position)):
            if (event.type == pygame.MOUSEBUTTONDOWN):
                self.is_selected = True

    def draw(self, master: pygame.Surface):
        if (self.is_selected):
            self.hitbox = pygame.draw.circle(master, Point.SELECTED_COLOR, (self.position.x,self.position.y), self.radius)
        else:
            self.hitbox = pygame.draw.circle(master, Point.UNSELECTED_COLOR, (self.position.x,self.position.y), self.radius)
        # master.blit(self.image, (self.position.x, self.position.y))


class Frame(Draw):
    def __init__(self) -> None:
        self.points: list[Point] = []
        self.is_selected: bool = False

class Timeline(pygame.sprite.Sprite, Draw, EventHandler):
    FRAME_MARGIN: int = 5
    def __init__(self, width: float, height: float, position: Position) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.frames: list[Frame] = []
        self.image = pygame.Surface([width, height])
        self.position: Position = position
        self.background_color: pygame.Color = pygame.Color(50, 50, 50)
        
        self.frame_texture: pygame.Surface = pygame.Surface((self.image.get_height()-(Timeline.FRAME_MARGIN*2), self.image.get_height()-(Timeline.FRAME_MARGIN*2)))
        self.frame_background_color: pygame.Color = pygame.Color(150,150,150)
        
    
    def draw(self, master: pygame.Surface):
        # Timeline
        self.image.fill(self.background_color)
        master.blit(self.image, (self.position.x, self.position.y))
        
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
    

class Video(Draw, EventHandler):
    def __init__(self) -> None:
        self.frames: list[Frame] = []

class WorkspaceBuilder(pygame.sprite.Sprite, Draw, EventHandler):
    def __init__(self, width: float, height: float, position: Position) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.frame: Frame|None = None
        self.image = pygame.Surface([width, height])
        self.width: float = width
        self.height: float = height
        self.position: Position = position
        self.hitbox: pygame.Rect = self.image.fill(pygame.Color(30, 30, 30))
        self.must_display_circle: bool = False
        self.must_display_line: bool = False
        self.is_dragging: bool = False
        self.selected_point: Point|None = None

    def draw(self, master: pygame.Surface):
        master.blit(self.image, (self.position.x, self.position.y))
        for point in self.frame.points:
            point.draw(master)
        
        if (len(self.frame.points) > 1):
            for point in self.frame.points:
                if (point.parent != None):
                    pygame.draw.line(master, pygame.Color(255,255,255), (point.parent.position.x, point.parent.position.y), (point.position.x, point.position.y))

        if (self.must_display_line):
            selected_points: list[Point] = [point for point in self.frame.points if point.is_selected]
            if (len(selected_points) > 0):
                selected_point = selected_points[0]
                parent: Point = selected_point.parent
                if (parent is not None):
                    origin: Position = Math.find_origin_point(parent.position, selected_point.position)
                    end: Position = Math.compute_new_point_using_x(origin, selected_point.position, self.image.get_width())
                    pygame.draw.line(master, pygame.Color(0,255,0), (origin.x, origin.y), (end.x, end.y))

        if (self.must_display_circle):
            selected_points: list[Point] = [point for point in self.frame.points if point.is_selected]
            if (len(selected_points) > 0):
                selected_point = selected_points[0]
                parent: Point = selected_point.parent
                if (parent is not None):
                    radius: float = sqrt((parent.position.x - selected_point.position.x)**2 + (parent.position.y - selected_point.position.y)**2)
                    pygame.draw.circle(master, pygame.Color(0,255,0), (parent.position.x, parent.position.y), radius, 1)


    def handle(self, event: pygame.event.Event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.frame.points.clear()
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE):
            selected_points: list[Point] = [point for point in self.frame.points if point.is_selected]
            if (len(selected_points) > 0):
                for point in selected_points:
                    self.frame.points.remove(point)
                    if (point.parent is not None):
                        point.parent.is_selected = True
                        self.selected_point = point.parent
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
                        self.selected_point = selected_point_with_mouse
                    else:
                        selected_points: list[Point] = [point for point in self.frame.points if point.is_selected]
                        for point in self.frame.points:
                            point.is_selected = False
                        new_point: Point = Point(Position(mouse_position[0],mouse_position[1]))
                        new_point.is_selected = True
                        self.selected_point = new_point
                        if (len(selected_points) > 0):
                            new_point.parent = selected_points[0]
                        self.frame.points.append(new_point)
                if (event.type == pygame.MOUSEBUTTONUP):
                    self.is_dragging = False
                if (event.type == pygame.MOUSEMOTION):
                    if (self.is_dragging):
                        print("Drag!")
                        self.selected_point.position.x = mouse_position[0]
                        self.selected_point.position.y = mouse_position[1]
                    if (self.must_display_line and self.selected_point is not None and self.selected_point.parent is not None):
                        parent: Point = self.selected_point.parent
                        print("..")
                        dx = self.image.get_width() - 0
                        dy = self.image.get_height() - 0
                        line_length = (dx ** 2 + dy ** 2) ** 0.5
                        if line_length > 0:
                            t = ((mouse_position[0] - 0) * dx + (mouse_position[1] - 0) * dy) / (line_length ** 2)
                            t = max(0, min(1, t))
                            point_x = 0 + t * dx
                            point_y = 0 + t * dy
                        point_x = int(parent.position.x + t * (self.selected_point.position.x - parent.position.x))
                        point_y = int(parent.position.y + t * (self.selected_point.position.y - parent.position.y))
                        self.selected_point.position.x = point_x
                        self.selected_point.position.y = point_y
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
        
        screen = pygame.display.set_mode((App.WINDOW_WIDTH, App.WINDOW_HEIGHT))
        clock = pygame.time.Clock()
        running = True
        
        frame: Frame = Frame()
        frame.is_selected = True
        workspace: WorkspaceBuilder = WorkspaceBuilder(App.WORKSPACE_WIDTH, App.WORKSPACE_HEIGHT, Position(0, 0))
        workspace.frame = frame
        video: Video = Video()
        video.frames.append(frame)
        timeline: Timeline = Timeline(App.TIMELINE_WIDTH, App.TIMELINE_HEIGHT, Position(0, App.WINDOW_HEIGHT-App.TIMELINE_HEIGHT))
        timeline.frames.append(frame)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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