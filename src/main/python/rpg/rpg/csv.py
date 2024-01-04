from pathlib import Path
from rpg.utils import Optional

class Csv:
    def __init__(self, data: list[list[object]], line_header: list[str]|None=None, column_header: list[str]|None=None) -> None:
        self.__line_header: list[str]|None = line_header
        self.__column_header: list[str]|None = column_header
        self.__data: list[list[object]] = data
    
    def get_line_headers(self) -> Optional[list[str]]:
        return Optional.of_nullable(self.__line_header)
    
    def get_column_headers(self) -> Optional[list[str]]:
        return Optional.of_nullable(self.__column_header)

    def get_line_by_header(self, header: str) -> Optional[list[object]]:
        line: list[object]|None = None
        for row in self.__data:
            if (str(row[0]).lower().strip() == header.lower().strip()):
                line = row[1:]
                break
        return Optional.of_nullable(line)
    
    def get_column_by_header(self, header: str) -> Optional[list[str]]:
        column: list[object]|None = None
        index: int = -1
        try:
            index: int = self.__data[0].index(header)
        except:
            pass
        else:
            column = []
            for row in self.__data:
                column.append(row[index])
        return Optional.of_nullable(column[1:])
    
class CsvReader:
    @staticmethod
    def read(csv_file: Path) -> Csv:
        header_line: list[str]|None = None
        header_column: list[str]|None = None
        full_csv_content: list[list[object]] = []
        with open(csv_file, 'r') as file:
            for line in file.readlines():
                csv_line: list[str] = line.split(',')
                csv_line = [cell.strip() for cell in csv_line]
                for index in range(len(csv_line)):
                    if (csv_line[index].isnumeric()):
                        csv_line[index] = int(csv_line[index])                        
                full_csv_content.append(csv_line)
        return Csv(full_csv_content, header_line, header_column)
