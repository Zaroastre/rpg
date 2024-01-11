from math import atan2, cos, degrees, sin, sqrt

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

    def copy(self):
        return Position(self.x, self.y, self.z)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, __o: object) -> bool:
        are_equal: bool = False
        if (isinstance(__o, Position)):
            are_equal = (__o.x == self.x) and (__o.y == self.y) and (__o.z == self.z)
        return are_equal

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    @staticmethod
    def are_equivalent(first, second, error_threshold: int=0) -> bool:
        if (first is None or not isinstance(first, Position)):
            raise ValueError()
        if (second is None or not isinstance(second, Position)):
            raise ValueError()
        result: bool = False
        if (second.x-error_threshold <= first.x and first.x <= second.x+error_threshold):
            if (second.y-error_threshold <= first.y and first.y <= second.y+error_threshold):
                result = True
        return result

class Shape:
    def __init__(self, points: list[Position]) -> None:
        pass

class Geometry:
    """Utilitary class that can be used to computes usefull algorythm for geometry computation.
    """

    @staticmethod
    def compute_slope(start: Position, end: Position) -> float:
        if (start == end):
            return None
        if (start.x == end.x):
            return float("inf")
        delta_y = end.y - start.y
        delta_x = end.x - start.x
        slope: float = delta_y / delta_x
        return slope

    @staticmethod
    def compute_origin_point(start: Position, end: Position) -> Position:
        """Compute the original point from the two given points.

        Args:
            point1 (Position): First point
            point2 (Position): Second point

        Returns:
            Position: The new computed position
        """
        slope: float = Geometry.compute_slope(start, end)
        COEFFICIENT = -1
        COEFFICIENT_OF_LINE = slope * start.x - COEFFICIENT * start.y
        X = COEFFICIENT_OF_LINE / slope
        Y = 0
        return Position(X, Y)

    @staticmethod
    def calculate_point_from_y(start: Position, end: Position, y: float) -> Position:
        """Compute new point using 2 existing points and knowing the Y position.

        Args:
            point1 (Position): Firsrt point
            point2 (Position): Second point
            y (float): Y position of the new position to compute

        Returns:
            Position: The computed position
        """
        # Vérifier si les points sont sur la même ligne horizontale
        if start.y == end.y and start.y != y:
            raise ValueError(
                "Les points ne forment pas une ligne horizontale à la hauteur de Y.")
        x: float = 0.0
        if start.y == end.y:
            x = (start.x + end.x) / 2
        else:
            x = start.x + (y - start.y) * (end.x -
                                             start.x) / (end.y - start.y)
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
    def compute_rotation_angle(reference_point: Position, start: Position, end: Position) -> float:
        angle = atan2(start.y - reference_point.y, start.x - reference_point.x) - \
            atan2(end.y - reference_point.y, end.x - reference_point.x)
        angle_degrees = degrees(angle)
        return angle_degrees

    @staticmethod
    def compute_rotation_point(point: Position, rotation_center: Position, angle: float) -> Position:
        relative_x: float = point.x - rotation_center.x
        relative_y: float = point.y - rotation_center.y
        rotated_x: float = relative_x * cos(angle) - relative_y * sin(angle)
        rotated_y: float = relative_x * sin(angle) + relative_y * cos(angle)

        return Position((rotated_x + rotation_center.x), (rotated_y + rotation_center.y))

    @staticmethod
    def compute_distance(start: Position, end: Position) -> float:
        return sqrt((start.x - end.x)**2 + (start.y - end.y)**2)

    @staticmethod
    def compute_new_point_using_speed(start: Position, end: Position, speed: float):
        # Calcul de la distance entre start et end
        distance: float = Geometry.compute_distance(start, end)
        if (distance == 0):
            return end.copy()

        # Calcul de la direction (vecteur unitaire) de la droite
        direction_x = (end.x - start.x) / distance
        direction_y = (end.y - start.y) / distance

        # Calcul des coordonnées du nouveau point
        new_point_x = end.x + (direction_x * speed)
        new_point_y = end.y + (direction_y * speed)

        # Création du nouveau point
        new_point = Position(new_point_x, new_point_y)
        return new_point

    @staticmethod
    def compute_angle(position_1: Position, position_2: Position) -> float:
        delta_x = position_2.x - position_1.x
        delta_y = position_2.y - position_1.y
        angle_rad: float = atan2(delta_y, delta_x)
        angle_deg: float = degrees(angle_rad)
        return angle_deg