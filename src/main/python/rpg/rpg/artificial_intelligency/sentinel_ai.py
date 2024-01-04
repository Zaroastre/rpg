from enum import Enum

from rpg.math.geometry import Position, Geometry
from rpg.artificial_intelligency.ai import ArtificialIntelligence

class SentinelEntity:
    def __init__(self, position: Position, radius: int, orientation: float, field_of_view: float, view_distance: int) -> None:
        self.__position: Position = position
        self.__radius: int = radius
        self.__orientation: float = orientation
        self.__field_of_view: float = field_of_view
        self.__view_distance: int = view_distance
    @property
    def position(self) -> Position:
        return self.__position
    @property
    def radius(self) -> int:
        return self.__radius
    @property
    def orientation(self) -> float:
        return self.__orientation
    @property
    def field_of_view(self) -> float:
        return self.__field_of_view
    @property
    def view_distance(self) -> float:
        return self.__view_distance

class SentinelState(Enum):
    PATROL=1
    ALERT=2
    ATTACK=3
    FLEE=4

class CharactersSituation:
    def __init__(self, character: SentinelEntity, other: SentinelEntity, current_state: SentinelState) -> None:
        self.__character: SentinelEntity = character
        self.__other: SentinelEntity = other
        self.__current_state: SentinelState = current_state
    @property
    def character(self) -> SentinelEntity:
        return self.__character
    @property
    def other(self) -> SentinelEntity:
        return self.__other
    @property
    def current_state(self) -> SentinelState:
        return self.__current_state
    
class SentinelAI(ArtificialIntelligence):
    def __init__(self) -> None:
        pass
    
    def __is_in_field_of_view(self, character: SentinelEntity, other: SentinelEntity) -> bool:
        is_in_field_of_view: bool = False
        angle = abs(character.orientation - Geometry.compute_angle(character.position, other.position))
        if (angle <= (character.field_of_view / 2)):
            is_in_field_of_view = True
        return is_in_field_of_view
    
    def predict(self, input_data: CharactersSituation) -> SentinelState:
        distance: float = Geometry.compute_distance(input_data.character.position, input_data.other.position)
        current_state: SentinelState = input_data.current_state
        state: SentinelState = SentinelState.PATROL
        character_can_see_other: bool = distance < input_data.character.view_distance
        is_other_in_field_of_view: bool = self.__is_in_field_of_view(input_data.character, input_data.other)
        
        if (current_state == SentinelState.PATROL):
            if (character_can_see_other and is_other_in_field_of_view):
                state = SentinelState.ALERT

        elif (current_state == SentinelState.ALERT):
            if (character_can_see_other and is_other_in_field_of_view):
                state = SentinelState.ATTACK

        elif (current_state == SentinelState.ATTACK):
            if (not character_can_see_other or not is_other_in_field_of_view):
                state = SentinelState.FLEE

        elif (current_state == SentinelState.FLEE):
            if (character_can_see_other and is_other_in_field_of_view):
                state = SentinelState.ALERT

        return state

def main():
    enemy = SentinelEntity(Position(0, 0), 50, 90.0, 120.0, 50)
    target = SentinelEntity(Position(0, 0), 50, 90.0, 120.0, 50)
    
    ia: SentinelAI = SentinelAI()
    previous_state: SentinelState = SentinelState.PATROL
    new_state: SentinelState = ia.predict(input_data=CharactersSituation(character=enemy, other=target, current_state=previous_state))
    

if (__name__ == "__main__"):
    main()