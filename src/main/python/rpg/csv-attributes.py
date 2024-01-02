from pathlib import Path

class CsvAttributesExtractor:
    def __init__(self) -> None:
        self.__agility_file: Path = Path("./resources/attributes/agility.csv")
        self.__intellect_file: Path = Path("./resources/attributes/intellect.csv")
        self.__spirit_file: Path = Path("./resources/attributes/spirit.csv")
        self.__stamina_file: Path = Path("./resources/attributes/stamina.csv")
        self.__strength_file: Path = Path("./resources/attributes/strength.csv")

    def __extract_attribute_for_class_from_file(self, class_name: str, file_path: Path) -> dict[int, int]:
        attribute_per_level: dict[int, int] = {}

        lines: list[str] = []
        with open(file_path, 'r') as file:
            lines = file.readlines()

        attribute_column_index: int = -1
        level_column_index: int = -1
        
        for line_number, line in enumerate(lines):
            columns: str = line.split(",")
            if (line_number == 0):
                for index in range(len(columns)):
                    if (columns[index].strip().lower() == "level"):
                        level_column_index = index
                        break
                for index in range(len(columns)):
                    if (columns[index].strip().lower() == class_name.lower()):
                        attribute_column_index = index
                        break
            else:
                attribute_per_level[int(columns[level_column_index].strip())] = int(columns[attribute_column_index].strip())
        
        return attribute_per_level

    def extract(self, class_name: str) -> dict[str, dict[int, int]]:
        attributes: dict[str, dict[int, int]] = {}
        agility: dict[int, int] = self.__extract_attribute_for_class_from_file(class_name, self.__agility_file)
        attributes["agility"] = agility
        intellect: dict[int, int] = self.__extract_attribute_for_class_from_file(class_name, self.__intellect_file)
        attributes["intellect"] = intellect
        spirit: dict[int, int] = self.__extract_attribute_for_class_from_file(class_name, self.__spirit_file)
        attributes["spirit"] = spirit
        stamina: dict[int, int] = self.__extract_attribute_for_class_from_file(class_name, self.__stamina_file)
        attributes["stamina"] = stamina
        strength: dict[int, int] = self.__extract_attribute_for_class_from_file(class_name, self.__strength_file)
        attributes["strength"] = strength
        return attributes

def main():
    class_to_process: str = "warrior"
    attributes_extractor: CsvAttributesExtractor = CsvAttributesExtractor()
    attributes: dict[str, dict[int, int]] = attributes_extractor.extract(class_to_process)
    print(attributes)

if (__name__ == "__main__"):
    main()