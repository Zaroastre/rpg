from enum import Enum
from rpg.gamedesign.interval_system import Range
from rpg.gamedesign.geolocation_system import Position
from rpg.utils import Optional
from rpg.math.geometry import Geometry

class BodyPartValue:
    def __init__(self, id: int, is_bone: bool) -> None:
        self.__id: int = id
        self.__is_bone: bool = is_bone
        self.__is_joint: bool = not self.__is_bone

    @property
    def id(self) -> int:
        return self.__id
    @property
    def is_bone(self) -> bool:
        return self.__is_bone
    @property
    def is_joint(self) -> bool:
        return self.__is_joint

class BodyPart(Enum):
    HORN=BodyPartValue(1, True)
    HEAD=BodyPartValue(10, True)
    NECK=BodyPartValue(20, False)
    LEFT_SHOULDER=BodyPartValue(1_000, False)
    RIGHT_SHOULDER=BodyPartValue(2_000, False)
    STERNUM_JOINT=BodyPartValue(30, False)
    STERNUM=BodyPartValue(40, True)
    LEFT_FOREARM=BodyPartValue(1_010, True)
    RIGHT_FOREARM=BodyPartValue(2_010, True)
    LEFT_ELBOW=BodyPartValue(1_020, False)
    RIGHT_ELBOW=BodyPartValue(2_020, False)
    LEFT_ARM=BodyPartValue(1_030, True)
    RIGHT_ARM=BodyPartValue(2_030, True)
    LEFT_WRIST=BodyPartValue(1_040, False)
    RIGHT_WRIST=BodyPartValue(2_040, False)
    LEFT_HAND=BodyPartValue(1_050, True)
    RIGHT_HAND=BodyPartValue(2_050, True)
    CHEST=BodyPartValue(50, True)
    BACK=BodyPartValue(60, True)
    LEFT_WING=BodyPartValue(3_000, True)
    RIGHT_WING=BodyPartValue(4_000, True)
    TAIL=BodyPartValue(70, True)
    PELVIS=BodyPartValue(80, True)
    PELVIS_JOINT=BodyPartValue(90, False)
    LEFT_HIP=BodyPartValue(5_000, False)
    RIGHT_HIP=BodyPartValue(6_000, False)
    LEFT_THIGH=BodyPartValue(5_010, True)
    RIGHT_THIGH=BodyPartValue(6_010, True)
    LEFT_KNEE=BodyPartValue(5_020, False)
    RIGHT_KNEE=BodyPartValue(6_020, False)
    LEFT_LEG=BodyPartValue(5_030, True)
    RIGHT_LEG=BodyPartValue(6_030, True)
    LEFT_ANKLE=BodyPartValue(5_040, False)
    RIGHT_ANKLE=BodyPartValue(6_040, False)
    LEFT_FOOT=BodyPartValue(5_050, True)
    RIGHT_FOOT=BodyPartValue(6_050, True)

class Morphology:
    def __init__(self, weight: Range, size: Range, head_proportion: Range, neck_proportion: Range, arm_proportion: Range, hand_proportion: Range, body_proportion: Range, leg_proportion: Range, foot_proportion: Range) -> None:
        
        self.__weight: Range = weight
        self.__size: Range = size
        
        self.__head_proportion: Range = head_proportion
        self.__neck_proportion: Range = neck_proportion
        self.__arm_propotrion: Range = arm_proportion
        self.__hand_proportion: Range = hand_proportion
        self.__body_proportion: Range = body_proportion
        self.__leg_propotrion: Range = leg_proportion
        self.__foot_proportion: Range = foot_proportion
    
    @property
    def weight(self) -> Range:
        return self.__weight
    @property
    def size(self) -> Range:
        return self.__size
    
    @property
    def head_proportion(self) -> Range:
        return self.__head_proportion
    @property
    def neck_proportion(self) -> Range:
        return self.__neck_proportion
    @property
    def arm_proportion(self) -> Range:
        return self.__arm_propotrion
    @property
    def hand_proportion(self) -> Range:
        return self.__hand_proportion
    @property
    def body_proportion(self) -> Range:
        return self.__body_proportion
    @property
    def leg_proportion(self) -> Range:
        return self.__leg_propotrion
    @property
    def foot_proportion(self) -> Range:
        return self.__foot_proportion


class Joint:
    TOTAL_CREATED: int = 0
    def __init__(self, position: Position, radius: int, body_part: BodyPart) -> None:
        Joint.TOTAL_CREATED += 1
        self.__name: str = "PNT-#"+body_part.name
        self.parent: Joint|None = None
        self.position: Position = position
        self.__is_selected: bool = False
        self.__body_part: BodyPart = body_part
        self.__radius: int = radius
        self.__children: list[Joint] = []

    @property
    def body_part(self) -> BodyPart:
        return self.__body_part

    @property
    def radius(self) -> int:
        return self.__radius

    def get_children(self) -> list:
        return self.__children

    def is_selected(self) -> bool:
        return self.__is_selected

    @property
    def name(self) -> str:
        return self.__name

    def select(self):
        self.__is_selected = True
    
    def unselect(self):
        self.__is_selected = False

    def __repr__(self) -> str:
        return f"{self.__name}(P={self.parent})"

class Bone:
    def __init__(self, start: Position, end: Position, thickness: float, body_part: BodyPart, radius: int=0) -> None:
        self.__start: Position = start
        self.__end: Position = end
        self.__radius: int = radius
        self.__thickness: float = thickness
        self.__body_part: BodyPart = body_part
        self.__parent: Optional[Bone] = Optional.empty()
        self.__children: list[Bone] = []

    @property
    def body_part(self) -> BodyPart:
        return self.__body_part
    @property
    def size(self) -> int:
        if (self.__radius != 0):
            result = self.__radius
        else:
            result = Geometry.compute_distance(self.__start, self.__end)
        return abs(result)
    
    
class Skeleton:
    def __init__(self, height: int, bones: list[Bone], joints: list[Joint]) -> None:
        self.__bones: list[Bone] = bones
        self.__joints: list[Joint] = joints
        self.__height: int = height
    
    @property
    def total_bones(self) -> int:
        return len(self.__bones)
    @property
    def total_joints(self) -> int:
        return len(self.__joints)
    @property
    def bones(self) -> list[Bone]:
        return self.__bones.copy()
    @property
    def joints(self) -> list[Joint]:
        return self.__joints.copy()
    
    @property
    def size(self) -> int:
        return self.__height
    
    @property
    def wingspan(self) ->int :
        left_wrist: Joint = [joint for joint in self.__joints if joint.body_part == BodyPart.LEFT_WRIST][0]
        right_wrist: Joint = [joint for joint in self.__joints if joint.body_part == BodyPart.RIGHT_WRIST][0]
        return right_wrist.position.x - left_wrist.position.x
    
    @property
    def corpulence(self) -> int:
        left_hip: Joint = [joint for joint in self.__joints if joint.body_part == BodyPart.LEFT_HIP][0]
        right_hip: Joint = [joint for joint in self.__joints if joint.body_part == BodyPart.RIGHT_HIP][0]
        pelvis: int = abs(right_hip.position.x - left_hip.position.x)
        return pelvis

class SkeletonFactory:
    proportion_coude = 0.33  # Proportion du bras pour le coude
    proportion_poignet = 0.67  # Proportion du bras pour le poignet
    
    @staticmethod
    def create_humanoid_skeleton(morphology: Morphology, height: int=0, weight: int = 0) -> Skeleton:
        if (morphology is None):
            raise ValueError()
        default_humanoid_body_height: int = height if (height > 0) else int((morphology.size.minimum + morphology.size.maximum)/2)
        default_humanoid_body_width: int = weight if (weight > 0) else int((morphology.weight.minimum + morphology.weight.maximum)/2)
        canvas_width: int = default_humanoid_body_height
        canvas_height: int = canvas_width
        middle_canvas_width: int = int(canvas_width/2)
        middle_canvas_height: int = int(canvas_height/2)
        
        middle_joints: list[BodyPart] = [part for part in list(BodyPart) if (not str(part.name).lower().startswith("left_")) and (not str(part.name).lower().startswith("right_")) and part.value.is_joint]
        middle_joints.sort(key=lambda x: x.value.id)

        top_left_joints: list[BodyPart] = [part for part in list(BodyPart) if str(part.name).lower().startswith("left_") and part.value.is_joint and (1_000 <= part.value.id < 2_000)]
        top_left_joints.sort(key=lambda x: x.value.id)

        bottom_left_joints: list[BodyPart] = [part for part in list(BodyPart) if str(part.name).lower().startswith("left_") and part.value.is_joint and (5_000 <= part.value.id < 6_000)]
        bottom_left_joints.sort(key=lambda x: x.value.id)

        top_right_joints: list[BodyPart] = [part for part in list(BodyPart) if str(part.name).lower().startswith("right_") and part.value.is_joint and (2_000 <= part.value.id < 3_000)]
        top_right_joints.sort(key=lambda x: x.value.id)

        bottom_right_joints: list[BodyPart] = [part for part in list(BodyPart) if str(part.name).lower().startswith("right_") and part.value.is_joint and (6_000 <= part.value.id < 7_000)]
        bottom_right_joints.sort(key=lambda x: x.value.id)


        middle_bones: list[BodyPart] = [part for part in list(BodyPart) if (not str(part.name).lower().startswith("left_")) and (not str(part.name).lower().startswith("right_")) and part.value.is_bone]
        middle_bones.sort(key=lambda x: x.value.id)
        
        left_bones: list[BodyPart] = [part for part in list(BodyPart) if str(part.name).lower().startswith("left_") and part.value.is_bone]
        left_bones.sort(key=lambda x: x.value.id)

        right_bones: list[BodyPart] = [part for part in list(BodyPart) if str(part.name).lower().startswith("right_") and part.value.is_bone]
        right_bones.sort(key=lambda x: x.value.id)

        joints: list[Joint] = []
        
        y_position: int = 0
        x_position: int = 0        
        
        head_height: int = int(default_humanoid_body_height * ((morphology.head_proportion.minimum + morphology.head_proportion.maximum)/2) / 100)
        neck_height: int = int(default_humanoid_body_height * ((morphology.neck_proportion.minimum + morphology.neck_proportion.maximum)/2) / 100)
        body_height: int = int(default_humanoid_body_height * ((morphology.body_proportion.minimum + morphology.body_proportion.maximum)/2) / 100)
        arm_height: int = int(default_humanoid_body_height * ((morphology.arm_proportion.minimum + morphology.arm_proportion.maximum)/2) / 100)
        hand_height: int = int(default_humanoid_body_height * ((morphology.hand_proportion.minimum + morphology.hand_proportion.maximum)/2) / 100)
        leg_height: int = int(default_humanoid_body_height * ((morphology.leg_proportion.minimum + morphology.leg_proportion.maximum)/2) / 100)
        foot_height: int = int(default_humanoid_body_height * ((morphology.foot_proportion.minimum + morphology.foot_proportion.maximum)/2) / 100)
        
        previous_joint: Joint|None = None
        sternum_joint: Joint|None = None
        pelvis_joint: Joint|None = None

        # Articulations du millieu du corps de l'humanoide.
        sternum_joint, pelvis_joint = SkeletonFactory.__create_joints_for_body_middle(middle_canvas_width, middle_joints, joints, head_height, neck_height, body_height, previous_joint)

        # Articulations des articulations du bras gauche
        previous_joint = sternum_joint
        SkeletonFactory.__create_joints_for_left_arm(default_humanoid_body_height, middle_canvas_width, top_left_joints, joints, head_height, neck_height, previous_joint)
        
        # Articulations des articulations du bras droithe
        previous_joint = sternum_joint
        SkeletonFactory.__create_joints_for_right_arm(default_humanoid_body_height, middle_canvas_width, top_right_joints, joints, head_height, neck_height, previous_joint)

        # Articulations des articulations de la jambe gauche
        previous_joint = pelvis_joint
        SkeletonFactory.__create_joints_for_left_leg(middle_canvas_width, bottom_left_joints, joints, head_height, neck_height, body_height, leg_height, previous_joint)
    
        # Articulations des articulations de la jambe droite
        previous_joint = pelvis_joint
        SkeletonFactory.__create_joints_for_right_leg(middle_canvas_width, bottom_right_joints, joints, head_height, neck_height, body_height, leg_height, previous_joint)
    
        bones: list[Bone] = []
        
        # Ossature du millieu du corps de l'humanoide.
        sternum_height: int = 1
        pelvis_height: int = 1
        for body_part_bone in middle_bones:
            if (body_part_bone not  in [BodyPart.HORN, BodyPart.TAIL]):
                position_start: Position
                position_end: Position
                if (body_part_bone == BodyPart.HEAD):
                    position_start = Position(((default_humanoid_body_width/2)-(head_height/2)), 0)
                    position_end = Position(((default_humanoid_body_width/2)+(head_height/2)), head_height)
                elif (body_part_bone == BodyPart.STERNUM):
                    position_start = Position(((default_humanoid_body_width/2)-(head_height/2)), head_height+neck_height)
                    position_end = Position(((default_humanoid_body_width/2)+(head_height/2)), head_height+neck_height+sternum_height)
                elif (body_part_bone == BodyPart.CHEST):
                    position_start = Position(((default_humanoid_body_width/2)-(weight/2)), head_height+neck_height+sternum_height)
                    position_end = Position(((default_humanoid_body_width/2)+(weight/2)), head_height+neck_height+sternum_height+body_height)
                elif (body_part_bone == BodyPart.PELVIS):
                    position_start = Position(int(default_humanoid_body_width / 2), head_height+neck_height+sternum_height+body_height)
                    position_end = Position(int((default_humanoid_body_width / 2) + (default_humanoid_body_width / 2)), head_height+neck_height+sternum_height+body_height+pelvis_height)

                bone: Bone = Bone(position_start, position_end, 10, body_part_bone)
                bones.append(bone)

        return Skeleton(default_humanoid_body_height, bones, joints)

    @staticmethod
    def __create_joints_for_right_leg(middle_canvas_width: int, bottom_right_joints: list[Joint], joints: list[Joint], head_height: int, neck_height: int, body_height: int, leg_height: int, previous_joint: Joint|None):
        for body_part_joint in bottom_right_joints:
            radius: int = 2
            if body_part_joint == BodyPart.RIGHT_HIP:
                x_position = middle_canvas_width+(head_height*1.25)
                y_position = head_height+neck_height+body_height
                radius = 5
            elif body_part_joint == BodyPart.RIGHT_KNEE:
                x_position = middle_canvas_width+(head_height*1.25)
                y_position = head_height+neck_height+body_height + (leg_height/2)
            elif body_part_joint == BodyPart.RIGHT_ANKLE:
                x_position = middle_canvas_width+(head_height*1.25)
                y_position = head_height+neck_height+body_height + leg_height

            position: Position = Position(x_position,  y_position)
            joint: Joint = Joint(position, radius, body_part_joint)
            if (previous_joint is not None):
                joint.parent = previous_joint
            previous_joint = joint
            joints.append(joint)

    @staticmethod
    def __create_joints_for_left_leg(middle_canvas_width: int, bottom_left_joints: list[Joint], joints: list[Joint], head_height: int, neck_height: int, body_height: int, leg_height: int, previous_joint: Joint|None):
        for body_part_joint in bottom_left_joints:
            radius: int = 2
            if body_part_joint == BodyPart.LEFT_HIP:
                x_position = middle_canvas_width-(head_height*1.25)
                y_position = head_height+neck_height+body_height
                radius = 5
            elif body_part_joint == BodyPart.LEFT_KNEE:
                x_position = middle_canvas_width-(head_height*1.25)
                y_position = head_height+neck_height+body_height + (leg_height/2)
            elif body_part_joint == BodyPart.LEFT_ANKLE:
                x_position = middle_canvas_width-(head_height*1.25)
                y_position = head_height+neck_height+body_height + leg_height

            position: Position = Position(x_position,  y_position)
            joint: Joint = Joint(position, radius, body_part_joint)
            if (previous_joint is not None):
                joint.parent = previous_joint
            previous_joint = joint
            joints.append(joint)

    @staticmethod
    def __create_joints_for_right_arm(default_humanoid_body_height, middle_canvas_width: int, top_right_joints: list[Joint], joints: list[Joint], head_height: int, neck_height: int, previous_joint: Joint|None):
        for body_part_joint in top_right_joints:
            radius: int = 2
            if body_part_joint == BodyPart.RIGHT_SHOULDER:
                x_position = middle_canvas_width+(head_height*1.75)
                y_position = head_height+neck_height
                radius = 5
            elif body_part_joint == BodyPart.RIGHT_ELBOW:
                x_position = middle_canvas_width + (default_humanoid_body_height * SkeletonFactory.proportion_coude)
                y_position = head_height + neck_height
            elif body_part_joint == BodyPart.RIGHT_WRIST:
                x_position = middle_canvas_width + (default_humanoid_body_height * SkeletonFactory.proportion_poignet)
                y_position = head_height + neck_height

            position: Position = Position(x_position,  y_position)
            joint: Joint = Joint(position, radius, body_part_joint)
            if (previous_joint is not None):
                joint.parent = previous_joint
            previous_joint = joint
            joints.append(joint)

    @staticmethod
    def __create_joints_for_left_arm(default_humanoid_body_height, middle_canvas_width: int, top_left_joints: list[Joint], joints: list[Joint], head_height: int, neck_height: int, previous_joint: Joint|None):
        for body_part_joint in top_left_joints:
            radius: int = 2
            if body_part_joint == BodyPart.LEFT_SHOULDER:
                x_position = middle_canvas_width-(head_height*1.75)
                y_position = head_height+neck_height
                radius = 5
            elif body_part_joint == BodyPart.LEFT_ELBOW:
                x_position = middle_canvas_width - (default_humanoid_body_height * SkeletonFactory.proportion_coude)
                y_position = head_height + neck_height
            elif body_part_joint == BodyPart.LEFT_WRIST:
                x_position = middle_canvas_width - (default_humanoid_body_height * SkeletonFactory.proportion_poignet)
                y_position = head_height + neck_height

            position: Position = Position(x_position,  y_position)
            joint: Joint = Joint(position, radius, body_part_joint)
            if (previous_joint is not None):
                joint.parent = previous_joint
            previous_joint = joint
            joints.append(joint)

    @staticmethod
    def __create_joints_for_body_middle(middle_canvas_width: int, middle_joints: list[Joint], joints: list[Joint], head_height: int, neck_height: int, body_height: int, previous_joint: Joint|None):
        for body_part_joint in middle_joints:
            radius: int = 2
            if body_part_joint == BodyPart.NECK:
                y_position = head_height
                radius = int(head_height/4)
            elif body_part_joint == BodyPart.STERNUM_JOINT:
                y_position = head_height + neck_height
            elif body_part_joint == BodyPart.PELVIS_JOINT:
                y_position = head_height + neck_height + body_height
            position: Position = Position(middle_canvas_width, y_position)
            joint: Joint = Joint(position, radius, body_part_joint)
            if (body_part_joint == BodyPart.STERNUM_JOINT):
                sternum_joint = joint
            elif (body_part_joint == BodyPart.PELVIS_JOINT):
                pelvis_joint = joint
            if (previous_joint is not None):
                joint.parent = previous_joint
            previous_joint = joint
            joints.append(joint)
        return sternum_joint, pelvis_joint