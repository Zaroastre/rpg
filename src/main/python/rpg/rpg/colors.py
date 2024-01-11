class Color:
    def __init__(self, red: int, green: int, blue: int, alpha: int = 255) -> None:
        self.__red: int = red
        self.__green: int = green
        self.__blue: int = blue
        self.__alpha: int = alpha
    @property
    def red(self) -> int:
        return self.__red
    @property
    def green(self) -> int:
        return self.__green
    @property
    def blue(self) -> int:
        return self.__blue
    @property
    def alpha(self) -> int:
        return self.__alpha
    def __repr__(self) -> str:
        return f"({self.red}, {self.green}, {self.blue}, {self.alpha})"
    
    def to_tuple(self) -> tuple[int, int, int, int]:
        return (self.red, self.green, self.blue, self.alpha)

    @staticmethod
    def from_rgba(red: int, green: int, blue: int, alpha: int):
        return Color(red, green, blue, alpha)
    
    @staticmethod
    def from_hexa(hexa_code: str):
        code: str = hexa_code if (not hexa_code.startswith("#")) else hexa_code[1:]
        if (len(code) == 6):
            code += "FF"
        red: int =  int(code[0:2], 16)
        green: int =  int(code[2:4], 16)
        blue: int =  int(code[4:6], 16)
        alpha: int =  int(code[6:8], 16)
        return Color.from_rgba(red, green, blue, alpha)
    

class ColorPallet:
    @staticmethod
    def generate_colors_pallet(first_color: Color, last_color: Color, total_colors: int) -> list[Color]:
        if (total_colors < 2):
            raise ValueError()
        colors: list[Color] = []
        colors.append(first_color)
        for counter in range(1, total_colors - 1):
            percentage = counter / (total_colors - 1)
            
            red = int((last_color.red - first_color.red) * percentage + first_color.red)
            green = int((last_color.green - first_color.green) * percentage + first_color.green)
            blue = int((last_color.blue - first_color.blue) * percentage + first_color.blue)
            alpha = int((last_color.alpha - first_color.alpha) * percentage + first_color.alpha)
            
            colors.append(Color(red, green, blue, alpha))
        colors.append(last_color)
        return colors
