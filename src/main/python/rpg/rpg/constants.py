from rpg.colors import Color
from rpg.gamedesign.geolocation_system import Position

FRAMES_PER_SECOND: int = 60
WINDOW_WIDTH: int = 1920
WINDOW_HEIGHT: int = 1080
BACKGROUND_COLOR: Color = Color(0, 0, 0)

# Group Panel
GROUP_PANEL_WIDTH: int = 300
GROUP_PANEL_HEIGHT: int = 600
GROUP_PANEL_POSITION: Position = Position(10, 10)

# Member Panel
MEMBER_PANEL_WIDTH: int = GROUP_PANEL_WIDTH
MEMBER_PANEL_HEIGHT: int = 40

# Action Panel
ACTION_PANEL_WIDTH: int = WINDOW_WIDTH/2
ACTION_PANEL_HEIGHT: int = 80
ACTION_PANEL_POSITION: Position = Position((WINDOW_WIDTH/2)-(ACTION_PANEL_WIDTH/2), WINDOW_HEIGHT-ACTION_PANEL_HEIGHT)

# Experience Panel
EXPERIENCE_PANEL_WIDTH: int = ACTION_PANEL_WIDTH
EXPERIENCE_PANEL_HEIGHT: int = 10
EXPERIENCE_PANEL_POSITION: Position = Position(ACTION_PANEL_POSITION.x, ACTION_PANEL_POSITION.y-EXPERIENCE_PANEL_HEIGHT)

# Experience Panel
SPELL_POPUP_WIDTH: int = 300
SPELL_POPUP_HEIGHT: int = 200
SPELL_POPUP_POSITION: Position = Position(WINDOW_WIDTH-SPELL_POPUP_WIDTH, WINDOW_HEIGHT-SPELL_POPUP_HEIGHT)


# Message Panel
MESSAGE_PANEL_WIDTH: int = 450
MESSAGE_PANEL_HEIGHT: int = 400
MESSAGE_PANEL_POSITION: Position = Position(0, WINDOW_HEIGHT-MESSAGE_PANEL_HEIGHT)

# HUD Target
HUD_TARGET_WIDTH: int = 20
HUD_TARGET_HEIGHT: int = 20
HUD_TARGET_THICKNESS: int = 5
HUD_TARGET_CORNER_LENGTH: int = 10
HUD_TARGET_COLOR: Color = Color(255, 0, 0)

RETURN_SPEED = 2
