import pygame
from rpg.ui.sprites import CharacterSprite
from rpg.gamedesign.geolocation_system import Position

class Camera:
    def __init__(self, screen: pygame.Surface) -> None:
        self.__disaply_surface: pygame.Surface = screen
        
        # Camera position and size
        self.__half_screen_width: float = self.__disaply_surface.get_width() // 2
        self.__half_screen_height: float = self.__disaply_surface.get_height() // 2
        camera_left: int = self.__half_screen_width // 2
        camera_top: int = self.__half_screen_height // 2
        self.__camera_position: Position = Position(camera_left, camera_top)
        self.__camera_width: int = self.__disaply_surface.get_width()-(self.__camera_position.x*2)
        self.__camera_height: int = self.__disaply_surface.get_height()-(self.__camera_position.y*2)
        self.__default_camera_rect: pygame.Rect =pygame.Rect(self.__camera_position.x, self.__camera_position.y, self.__camera_width, self.__camera_height)
        self.__camera_rect: pygame.Rect = self.__default_camera_rect.copy()
        
        self.__camera_move_speed: float = 5.0
        
        # Zoom
        self.__default_zoom_scale: float = 1.0
        self.__zoom_scale: float = self.__default_zoom_scale
        self.__maximum_zoom_in: float = 0.5
        self.__maximum_zoom_out: float = 1.5
        self.__zoom_value: float = 0.1
        
        self.__target_to_track: pygame.sprite.Sprite = None
        
    @property
    def position(self) -> Position:
        return self.__camera_position
    @property
    def width(self) -> float:
        return self.__camera_width
    @property
    def height(self) -> float:
        return self.__camera_height
    @property
    def rect(self) -> pygame.Rect:
        return self.__camera_rect
    @property
    def target(self) -> pygame.sprite.Sprite:
        return self.__target_to_track
    
    def zoom_in(self):
        if (self.__zoom_scale < self.__maximum_zoom_out):
            self.__zoom_scale += self.__zoom_value
    
    def zoom_out(self):
        if (self.__zoom_scale > self.__maximum_zoom_in):
            self.__zoom_scale -= self.__zoom_value
    def reset_zoom(self):
        self.__zoom_scale = self.__default_zoom_scale

    def move_camera_on_left(self):
        self.__camera_rect.x -= self.__camera_move_speed
    def move_camera_on_right(self):
        self.__camera_rect.x += self.__camera_move_speed
    def move_camera_on_top(self):
        self.__camera_rect.y -= self.__camera_move_speed
    def move_camera_on_bottom(self):
        self.__camera_rect.y += self.__camera_move_speed
    def reset_camera_position(self):
        self.__camera_rect = self.__default_camera_rect.copy()
    
    def track(self, target: pygame.sprite.Sprite):
        self.__target_to_track = target
    
    def untrack(self):
        self.__target_to_track = None
    
class CameraGroup(pygame.sprite.Group):
    def __init__(self, master: pygame.Surface) -> None:
        super().__init__()
        self.__screen: pygame.Surface = master
        
        self.__offset: pygame.math.Vector2 = pygame.math.Vector2()
        
        self.__half_screen_width: float = self.__screen.get_width() // 2
        self.__half_screen_height: float = self.__screen.get_height() // 2
        camera_left: int = self.__half_screen_width // 2
        camera_top: int = self.__half_screen_height // 2
        self.__camera_position: Position = Position(camera_left, camera_top)
        self.__camera_width: int = self.__screen.get_width()-(self.__camera_position.x*2)
        self.__camera_height: int = self.__screen.get_height()-(self.__camera_position.y*2)
        self.__camera_rect: pygame.Rect = pygame.Rect(self.__camera_position.x, self.__camera_position.y, self.__camera_width, self.__camera_height)
        
        self.__camera_move_speed: float = 5.0
        
        self.__ground_surface: pygame.Surface = pygame.Surface((8_250, 19_000))
        # self.__ground_surface: pygame.Surface = pygame.Surface((8_000, 22_000))
        self.__ground_surface.fill(pygame.Color(0,50,200))
        self.__ground_rect: pygame.Rect = self.__ground_surface.get_rect(topleft=(0,0))
        self.__sprite_to_track: CharacterSprite = None

        self.__zoom_scale: float = 1.0
        self.__maximum_zoom_in: float = 0.5
        self.__maximum_zoom_out: float = 1.5
        self.__zoom_value: float = 0.1
        self.internal_surface_size: tuple[int, int] = (2500,2500)
        self.internal_surface: pygame.Surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect: pygame.Rect = self.internal_surface.get_rect(center=(self.__half_screen_width, self.__half_screen_height))
        self.internal_suface_size_vector: pygame.math.Vector2 = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset: pygame.math.Vector2 = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.__half_screen_width
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.__half_screen_height
    
    def set_character_to_track(self, character_sprite: CharacterSprite):
        self.__sprite_to_track = character_sprite
    
    def box_target_camera(self):
        if (self.__sprite_to_track is not None):
            if (self.__sprite_to_track.rect.left < self.__camera_rect.left):
                self.__camera_rect.left = self.__sprite_to_track.rect.left
            if (self.__sprite_to_track.rect.right > self.__camera_rect.right):
                self.__camera_rect.right = self.__sprite_to_track.rect.right
            if (self.__sprite_to_track.rect.bottom > self.__camera_rect.bottom):
                self.__camera_rect.bottom = self.__sprite_to_track.rect.bottom
            if (self.__sprite_to_track.rect.top < self.__camera_rect.top):
                self.__camera_rect.top = self.__sprite_to_track.rect.top
            self.__offset.x = self.__camera_rect.left - self.__camera_position.x
            self.__offset.y = self.__camera_rect.top - self.__camera_position.y
    
    def zoom_in(self):
        if (self.__zoom_scale < self.__maximum_zoom_out):
            self.__zoom_scale += self.__zoom_value
    
    def zoom_out(self):
        if (self.__zoom_scale > self.__maximum_zoom_in):
            self.__zoom_scale -= self.__zoom_value
    
    def move_camera_on_left(self):
        self.__camera_rect.x -= self.__camera_move_speed
    def move_camera_on_right(self):
        self.__camera_rect.x += self.__camera_move_speed
    def move_camera_on_top(self):
        self.__camera_rect.y -= self.__camera_move_speed
    def move_camera_on_bottom(self):
        self.__camera_rect.y += self.__camera_move_speed
    
    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_p]):
            self.zoom_in()
        if (keys[pygame.K_m]):
            self.zoom_in()
    
    def __update_offset(self):
        self.__offset.x = self.__sprite_to_track.rect.centerx - self.__half_screen_width
        self.__offset.y = self.__sprite_to_track.rect.centery - self.__half_screen_height

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a]):
            self.move_camera_on_left()
        if (keys[pygame.K_e]):
            self.move_camera_on_right()
        if (keys[pygame.K_r]):
            self.move_camera_on_top()
        if (keys[pygame.K_f]):
            self.move_camera_on_bottom()
                
        if (self.__sprite_to_track is not None):
            self.__update_offset()
    
    def __center_camera_on_target_to_track(self):
        if (self.__sprite_to_track is not None):
            self.__offset.x = self.__sprite_to_track.rect.centerx - self.__half_screen_width
            self.__offset.y = self.__sprite_to_track.rect.centery - self.__half_screen_height
    
    def handle(self):
        self.zoom_keyboard_control()
        self.keyboard_control()
        self.__center_camera_on_target_to_track()
        # self.box_target_camera()

    def draw(self, master: pygame.Surface):
        # self.internal_surface.fill(pygame.Color(0,50,200))
        # Ground
        ground_offset = self.__ground_rect.topleft - self.__offset + self.internal_offset
        self.internal_surface.blit(self.__ground_surface, ground_offset)
        
        # Active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.__offset + self.internal_offset
            sprite.offset = self.__offset
            sprite.draw(self.internal_surface)
            # self.__screen.blit(sprite.image, offset_possition)
        scaled_surface = pygame.transform.scale(self.internal_surface, self.internal_suface_size_vector*self.__zoom_scale)
        scaled_rect = scaled_surface.get_rect(center=(self.__half_screen_width, self.__half_screen_height))
        self.__screen.blit(scaled_surface, scaled_rect)
        master.blit(self.__screen, (0,0))
        pygame.draw.rect(self.__screen, pygame.Color(255,0,0), self.__camera_rect, 1)
