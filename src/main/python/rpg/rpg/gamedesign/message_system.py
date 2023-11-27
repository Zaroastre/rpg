from rpg.utils import SingletonMeta


class MessageBroker(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.__player_resource_messages: list[str] = []

        self.__player_experience_messages: list[str] = []

        self.__enemies_damages_messages: list[str] = []
        self.__enemies_cures_messages: list[str] = []

        self.__friends_damages_messages: list[str] = []
        self.__friends_cures_messages: list[str] = []

        self.__debug_messages: list[str] = []
        self.__system_messages: list[str] = []
    
    def __add_message(self, message: str, messages: list[str]):
        if (message is not None):
            if (len(messages) == 0) or (len(messages) > 0 and messages[-1] != message):
                messages.append(message)
            
    def add_player_resource_message(self, message: str):
        if (message is not None):
            self.__add_message(message, self.__player_resource_messages)
    
    def add_enemies_damages_message(self, message: str):
        if (message is not None):
            self.__add_message(message, self.__enemies_damages_messages)
    def add_enemies_cures_message(self, message: str):
        if (message is not None):
            self.__add_message(message, self.__enemies_cures_messages)
    def add_friends_damages_message(self, message: str):
        if (message is not None):
            self.__add_message(message, self.__friends_damages_messages)
    def add_friends_cures_message(self, message: str):
        if (message is not None):
            self.__add_message(message, self.__friends_cures_messages)
    def add_debug_message(self, message: str):
        if (message is not None):
            self.__add_message(message, self.__debug_messages)
    def add_system_message(self, message: str):
        if (message is not None):
            self.__add_message(message, self.__system_messages)
            
    def __get_message(self, messages: list[str]) -> list[str]:
        message_to_read: list[str] = []
        if (len(messages) > 0):
            message_to_read = messages.copy()
            messages.clear()
        return message_to_read
    
    def get_player_resource_message(self) -> list[str]:
        return self.__get_message(self.__player_resource_messages)
    def get_player_experiene_message(self) -> list[str]:
        return self.__get_message(self.__player_experience_messages)
    def get_enemies_damages_message(self) -> list[str]:
        return self.__get_message(self.__enemies_damages_messages)
    def get_enemies_cures_message(self) -> list[str]:
        return self.__get_message(self.__enemies_cures_messages)
    def get_friends_damages_message(self) -> list[str]:
        return self.__get_message(self.__friends_damages_messages)
    def get_friends_cures_message(self) -> list[str]:
        return self.__get_message(self.__friends_cures_messages)
    def get_debug_message(self) -> list[str]:
        return self.__get_message(self.__debug_messages)
    def get_system_message(self) -> list[str]:
        return self.__get_message(self.__system_messages)