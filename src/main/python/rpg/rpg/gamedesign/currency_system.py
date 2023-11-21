class Currency:
    MAXIMUM_SILVER: int = 100
    MAXIMUM_COPPER: int = 100
    def __init__(self) -> None:
        self.__copper: int = 0
        self.__silver: int = 0
        self.__gold: int = 0
    
    @property
    def copper(self) -> int:
        return self.__copper
    @property
    def silver(self) -> int:
        return self.__silver
    @property
    def gold(self) -> int:
        return self.__gold
    
    def add_currency(self, copper: int, silver: int, gold: int):
        if any(currency is None or currency < 0 for currency in [copper, silver, gold]):
            raise ValueError("Currency values cannot be negative or None.")
        
        total_copper = self.__copper + copper
        total_silver = self.__silver + silver + total_copper // Currency.MAXIMUM_COPPER
        total_gold = self.__gold + gold + total_silver // Currency.MAXIMUM_SILVER

        self.__copper = total_copper % Currency.MAXIMUM_COPPER
        self.__silver = total_silver % Currency.MAXIMUM_SILVER
        self.__gold = total_gold

    def remove_currency(self, copper: int, silver: int, gold: int):
        if any(currency is None or currency < 0 for currency in [copper, silver, gold]):
            raise ValueError("Currency values cannot be negative or None.")

        total_copper = self.__copper - copper
        total_silver = self.__silver - silver
        total_gold = self.__gold - gold

        if total_copper < 0:
            borrowed_silver = (-total_copper - 1) // Currency.MAXIMUM_COPPER + 1
            total_silver -= borrowed_silver
            total_copper += borrowed_silver * Currency.MAXIMUM_COPPER

        if total_silver < 0:
            borrowed_gold = (-total_silver - 1) // Currency.MAXIMUM_SILVER + 1
            total_gold -= borrowed_gold
            total_silver += borrowed_gold * Currency.MAXIMUM_SILVER

        if total_gold < 0:
            raise ValueError("Insufficient gold.")

        self.__copper = total_copper
        self.__silver = total_silver
        self.__gold = total_gold

    def had_enought_currency(self, copper: int, silver: int, gold: int) -> bool:
        if any(val is None or val < 0 for val in [copper, silver, gold]):
            raise ValueError("Currency values cannot be negative or None.")

        total_copper = self.__copper - copper
        total_silver = self.__silver - silver
        total_gold = self.__gold - gold

        if total_copper < 0:
            borrowed_silver = (-total_copper - 1) // Currency.MAXIMUM_COPPER + 1
            total_silver -= borrowed_silver
            total_copper += borrowed_silver * Currency.MAXIMUM_COPPER

        if total_silver < 0:
            borrowed_gold = (-total_silver - 1) // Currency.MAXIMUM_SILVER + 1
            total_gold -= borrowed_gold
            total_silver += borrowed_gold * Currency.MAXIMUM_SILVER

        return total_copper >= 0 and total_silver >= 0 and total_gold >= 0
