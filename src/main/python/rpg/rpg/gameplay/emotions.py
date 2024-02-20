from abc import ABC, abstractmethod
from enum import Enum
from random import randint

class Singleton(type):
    _instances = {}
    # we are going to redefine (override) what it means to "call" a class
    # as in ....  x = MyClass(1,2,3)
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # we have not every built an instance before.  Build one now.
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        else:
            instance = cls._instances[cls]
            # here we are going to call the __init__ and maybe reinitialize.
            if hasattr(cls, '__allow_reinitialization') and cls.__allow_reinitialization:
                # if the class allows reinitialization, then do it
                instance.__init__(*args, **kwargs)  # call the init again
        return instance

class Emotion:
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

class Intensity:
    LOW: int = 0
    MEDIUM: int = 1
    HIGH: int = 2
    SEVERAL: int = 3

    MINIMUM: int = 0
    MAXIMUM: int = 3

    @abstractmethod
    def can_increase_intensity(self) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def can_decrease_intensity(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def increase_intensity(self) -> Emotion:
        raise NotImplementedError()
    @abstractmethod
    def decrease_intensity(self) -> Emotion:
        raise NotImplementedError()

    @abstractmethod
    def is_primary_emotion(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_secondary_emotion(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_complexe_emotion(self) -> bool:
        raise NotImplementedError()

class DefaultEmotion(Emotion, Intensity, metaclass=Singleton):
    def __init__(self, name: str, intensity: int) -> None:
        self.__name: str = name
        self.__intensity: int = intensity

    @property
    def name(self) -> str:
        return self.__name
    @property
    def intensity(self) -> int:
        return self.__intensity
    def get_name(self) -> str:
        return self.name

    def can_increase_intensity(self) -> bool:
        return self.__intensity < Intensity.MAXIMUM
    def can_decrease_intensity(self) -> bool:
        return self.__intensity > Intensity.MINIMUM
    def is_primary_emotion(self) -> bool:
        return self.__intensity == 1
    def is_secondary_emotion(self) -> bool:
        return self.__intensity == 2
    def is_complexe_emotion(self) -> bool:
        return self.__intensity == 3

    def feel_fear(self) -> 'FearEmotion':
        return FearEmotion()
    def feel_love(self) -> 'LoveEmotion':
        return LoveEmotion()
    def feel_joy(self) -> 'JoyEmotion':
        return JoyEmotion()
    def feel_anger(self) -> 'AngerEmotion':
        return AngerEmotion()
    def feel_sadness(self) -> 'SadnessEmotion':
        return SadnessEmotion()
    def feel_surprise(self) -> 'SurpriseEmotion':
        return SurpriseEmotion()

class NeutralEmotion(DefaultEmotion):
    def __init__(self, name: str="Neutral", intensity: int=Intensity.LOW) -> None:
        super().__init__(name, intensity)

    def decrease_intensity(self) -> Emotion:
        if self == NeutralEmotion():
            return self

        emotions_tree: EmotionsTree = EmotionsTree()
        emotions_categories: dict[Emotion, list[Emotion]] = {
            FearEmotion(): list(emotions_tree.fear.keys()),
            AngerEmotion(): list(emotions_tree.anger.keys()),
            JoyEmotion(): list(emotions_tree.joy.keys()),
            LoveEmotion(): list(emotions_tree.love.keys()),
            SurpriseEmotion(): list(emotions_tree.surprise.keys()),
            SadnessEmotion(): list(emotions_tree.sadness.keys())
        }

        for emotions_category, emotions_list in emotions_categories.items():
            if self == emotions_category or self in emotions_list:
                return NeutralEmotion()
            else:
                for known_emotion in emotions_list:
                    if self in emotions_tree.get(known_emotion):
                        return known_emotion
        return NeutralEmotion()

    def increase_intensity(self) -> Emotion:
        emotions_tree: EmotionsTree = EmotionsTree()
        available_emotions: list[Emotion] = emotions_tree.get(self)
        if (len(available_emotions) > 0):
            return available_emotions[randint(0, len(available_emotions)-1)]
        return self

class FearEmotion(NeutralEmotion):
    def __init__(self, name: str="Fear", intensity: int=Intensity.MEDIUM) -> None:
        super().__init__(name, intensity)

class ScaredEmotion(FearEmotion):
    def __init__(self, name: str="Scared", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class FrightenedEmotion(ScaredEmotion):
    def __init__(self) -> None:
        super().__init__("Frightened", intensity=Intensity.SEVERAL)
class HelplessEmotion(ScaredEmotion):
    def __init__(self) -> None:
        super().__init__("Helpless", intensity=Intensity.SEVERAL)

class TerrorEmotion(FearEmotion):
    def __init__(self, name: str="Terror", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class HystericalEmotion(TerrorEmotion):
    def __init__(self) -> None:
        super().__init__("Hysterical", intensity=Intensity.SEVERAL)
class PanicEmotion(TerrorEmotion):
    def __init__(self) -> None:
        super().__init__("Panic", intensity=Intensity.SEVERAL)

class InsecureEmotion(FearEmotion):
    def __init__(self, name: str="Insecure", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class InadequateEmotion(InsecureEmotion):
    def __init__(self) -> None:
        super().__init__("Inadequate", intensity=Intensity.SEVERAL)
class InferiorEmotion(InsecureEmotion):
    def __init__(self) -> None:
        super().__init__("Inferior", intensity=Intensity.SEVERAL)

class NervousEmotion(FearEmotion):
    def __init__(self, name: str="Nervous", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class AnxiousEmotion(NervousEmotion):
    def __init__(self) -> None:
        super().__init__("Anxious", intensity=Intensity.SEVERAL)
class WorriedEmotion(NervousEmotion):
    def __init__(self) -> None:
        super().__init__("Worried", intensity=Intensity.SEVERAL)

class HorrorEmotion(FearEmotion):
    def __init__(self, name: str="Horror", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class DreadEmotion(HorrorEmotion):
    def __init__(self) -> None:
        super().__init__("Dread", intensity=Intensity.SEVERAL)
class MortifiedEmotion(HorrorEmotion):
    def __init__(self) -> None:
        super().__init__("Mortified", intensity=Intensity.SEVERAL)


class LoveEmotion(NeutralEmotion):
    def __init__(self, name: str="Love", intensity: int=Intensity.MEDIUM) -> None:
        super().__init__(name, intensity)

class PeacefulEmotion(LoveEmotion):
    def __init__(self, name: str="Peaceful", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class SatisfiedEmotion(PeacefulEmotion):
    def __init__(self) -> None:
        super().__init__("Satisfied", intensity=Intensity.SEVERAL)
class RelievedEmotion(PeacefulEmotion):
    def __init__(self) -> None:
        super().__init__("Relieved", intensity=Intensity.SEVERAL)

class TendernessEmotion(LoveEmotion):
    def __init__(self, name: str="Tenderness", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class CompassionateEmotion(TendernessEmotion):
    def __init__(self) -> None:
        super().__init__("Compassionate", intensity=Intensity.SEVERAL)
class CaringEmotion(TendernessEmotion):
    def __init__(self) -> None:
        super().__init__("Caring", intensity=Intensity.SEVERAL)

class DesireEmotion(LoveEmotion):
    def __init__(self, name: str="Desire", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class InfaturationEmotion(DesireEmotion):
    def __init__(self) -> None:
        super().__init__("Infaturation", intensity=Intensity.SEVERAL)
class PassionEmotion(DesireEmotion):
    def __init__(self) -> None:
        super().__init__("Passion", intensity=Intensity.SEVERAL)

class LongingEmotion(LoveEmotion):
    def __init__(self, name: str="Longing", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class AttractedEmotion(LongingEmotion):
    def __init__(self) -> None:
        super().__init__("Attracted", intensity=Intensity.SEVERAL)
class SentimentalEmotion(LongingEmotion):
    def __init__(self) -> None:
        super().__init__("Sentimental", intensity=Intensity.SEVERAL)

class AffectionnateEmotion(LoveEmotion):
    def __init__(self, name: str="Affectionnate", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class FondnessEmotion(AffectionnateEmotion):
    def __init__(self) -> None:
        super().__init__("Fondness", intensity=Intensity.SEVERAL)
class RomanticEmotion(AffectionnateEmotion):
    def __init__(self) -> None:
        super().__init__("Romantic", intensity=Intensity.SEVERAL)


class JoyEmotion(NeutralEmotion):
    def __init__(self, name: str="Joy", intensity: int=Intensity.MEDIUM) -> None:
        super().__init__(name, intensity)

class EnthralledEmotion(JoyEmotion):
    def __init__(self, name: str="Enthralled", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class RaptureEmotion(EnthralledEmotion):
    def __init__(self) -> None:
        super().__init__("Rapture", intensity=Intensity.SEVERAL)
class EnchantedEmotion(EnthralledEmotion):
    def __init__(self) -> None:
        super().__init__("Enchanted", intensity=Intensity.SEVERAL)

class ElationEmotion(JoyEmotion):
    def __init__(self, name: str="Elation", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class JubilationEmotion(ElationEmotion):
    def __init__(self) -> None:
        super().__init__("Jubilation", intensity=Intensity.SEVERAL)
class EuphoricEmotion(ElationEmotion):
    def __init__(self) -> None:
        super().__init__("Euphoric", intensity=Intensity.SEVERAL)

class EnthusiasticEmotion(JoyEmotion):
    def __init__(self, name: str="Enthusiastic", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class ZealEmotion(EnthusiasticEmotion):
    def __init__(self) -> None:
        super().__init__("Zeal", intensity=Intensity.SEVERAL)
class ExcitedEmotion(EnthusiasticEmotion):
    def __init__(self) -> None:
        super().__init__("Excited", intensity=Intensity.SEVERAL)

class OptimisticEmotion(JoyEmotion):
    def __init__(self, name: str="Optimistic", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class HopefulEmotion(OptimisticEmotion):
    def __init__(self) -> None:
        super().__init__("Hopeful", intensity=Intensity.SEVERAL)
class EagerEmotion(OptimisticEmotion):
    def __init__(self) -> None:
        super().__init__("Eager", intensity=Intensity.SEVERAL)

class ProudEmotion(JoyEmotion):
    def __init__(self, name: str="Proud", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class IllustriousEmotion(ProudEmotion):
    def __init__(self) -> None:
        super().__init__("Illustrious", intensity=Intensity.SEVERAL)
class TriumphantEmotion(ProudEmotion):
    def __init__(self) -> None:
        super().__init__("Triumphant", intensity=Intensity.SEVERAL)

class CheerfulEmotion(JoyEmotion):
    def __init__(self, name: str="Cheerful", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class BlissfulEmotion(CheerfulEmotion):
    def __init__(self) -> None:
        super().__init__("Blissful", intensity=Intensity.SEVERAL)
class JovialEmotion(CheerfulEmotion):
    def __init__(self) -> None:
        super().__init__("Jovial", intensity=Intensity.SEVERAL)

class HappyEmotion(JoyEmotion):
    def __init__(self, name: str="Happy", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class DelightedEmotion(HappyEmotion):
    def __init__(self) -> None:
        super().__init__("Delighted", intensity=Intensity.SEVERAL)
class AmusedEmotion(HappyEmotion):
    def __init__(self) -> None:
        super().__init__("Amused", intensity=Intensity.SEVERAL)

class ContentEmotion(JoyEmotion):
    def __init__(self, name: str="Content", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class PleasedEmotion(ContentEmotion):
    def __init__(self) -> None:
        super().__init__("Pleased", intensity=Intensity.SEVERAL)
class VerySatisfiedEmotion(ContentEmotion):
    def __init__(self) -> None:
        super().__init__("VerySatisfied", intensity=Intensity.SEVERAL)


class AngerEmotion(NeutralEmotion):
    def __init__(self, name: str="Anger", intensity: int=Intensity.MEDIUM) -> None:
        super().__init__(name, intensity)

class RageEmotion(AngerEmotion):
    def __init__(self, name: str="Rage", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class HateEmotion(RageEmotion):
    def __init__(self) -> None:
        super().__init__("Hate", intensity=Intensity.SEVERAL)
class HostileEmotion(RageEmotion):
    def __init__(self) -> None:
        super().__init__("Hostile", intensity=Intensity.SEVERAL)

class ExasperatedEmotion(AngerEmotion):
    def __init__(self, name: str="Exasperated", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class AgitatedEmotion(ExasperatedEmotion):
    def __init__(self) -> None:
        super().__init__("Agitated", intensity=Intensity.SEVERAL)
class FrustratedEmotion(ExasperatedEmotion):
    def __init__(self) -> None:
        super().__init__("Frustrated", intensity=Intensity.SEVERAL)

class IrritableEmotion(AngerEmotion):
    def __init__(self, name: str="Irritable", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class AnnoyedEmotion(IrritableEmotion):
    def __init__(self) -> None:
        super().__init__("Annoyed", intensity=Intensity.SEVERAL)
class AggravatedEmotion(IrritableEmotion):
    def __init__(self) -> None:
        super().__init__("Aggravated", intensity=Intensity.SEVERAL)

class EnvyEmotion(AngerEmotion):
    def __init__(self, name: str="Envy", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class ResentfulEmotion(EnvyEmotion):
    def __init__(self) -> None:
        super().__init__("Resentful", intensity=Intensity.SEVERAL)
class JealousEmotion(EnvyEmotion):
    def __init__(self) -> None:
        super().__init__("Jealous", intensity=Intensity.SEVERAL)

class DisgustEmotion(AngerEmotion):
    def __init__(self, name: str="Disgust", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class ContemptEmotion(DisgustEmotion):
    def __init__(self) -> None:
        super().__init__("Contempt", intensity=Intensity.SEVERAL)
class RevoltedEmotion(DisgustEmotion):
    def __init__(self) -> None:
        super().__init__("Revolted", intensity=Intensity.SEVERAL)


class SadnessEmotion(NeutralEmotion):
    def __init__(self, name: str="Sadness", intensity: int=Intensity.MEDIUM) -> None:
        super().__init__(name, intensity)

class SufferingEmotion(SadnessEmotion):
    def __init__(self, name: str="Suffering", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class AgonyEmotion(SufferingEmotion):
    def __init__(self) -> None:
        super().__init__("Agony", intensity=Intensity.SEVERAL)
class HurtEmotion(SufferingEmotion):
    def __init__(self) -> None:
        super().__init__("Hurt", intensity=Intensity.SEVERAL)

class VerySadnessEmotion(SadnessEmotion):
    def __init__(self, name: str="VerySadness", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class DepressedEmotion(VerySadnessEmotion):
    def __init__(self) -> None:
        super().__init__("Depressed", intensity=Intensity.SEVERAL)
class SorrowEmotion(VerySadnessEmotion):
    def __init__(self) -> None:
        super().__init__("Sorrow", intensity=Intensity.SEVERAL)

class DisappointedEmotion(SadnessEmotion):
    def __init__(self, name: str="Disappointed", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class DismayedEmotion(DisappointedEmotion):
    def __init__(self) -> None:
        super().__init__("Dismayed", intensity=Intensity.SEVERAL)
class DispleasedEmotion(DisappointedEmotion):
    def __init__(self) -> None:
        super().__init__("Displeased", intensity=Intensity.SEVERAL)

class ShamefulEmotion(SadnessEmotion):
    def __init__(self, name: str="Shameful", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class RegretfulEmotion(ShamefulEmotion):
    def __init__(self) -> None:
        super().__init__("Regretful", intensity=Intensity.SEVERAL)
class GuityEmotion(ShamefulEmotion):
    def __init__(self) -> None:
        super().__init__("Guity", intensity=Intensity.SEVERAL)

class NeglectedEmotion(SadnessEmotion):
    def __init__(self, name: str="Neglected", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class IsolatedEmotion(NeglectedEmotion):
    def __init__(self) -> None:
        super().__init__("Isolated", intensity=Intensity.SEVERAL)
class LonelyEmotion(NeglectedEmotion):
    def __init__(self) -> None:
        super().__init__("Lonely", intensity=Intensity.SEVERAL)

class DespairEmotion(SadnessEmotion):
    def __init__(self, name: str="Despair", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class GriefEmotion(DespairEmotion):
    def __init__(self) -> None:
        super().__init__("Grief", intensity=Intensity.SEVERAL)
class PowerlessEmotion(DespairEmotion):
    def __init__(self) -> None:
        super().__init__("Powerless", intensity=Intensity.SEVERAL)


class SurpriseEmotion(NeutralEmotion):
    def __init__(self, name: str="Surprise", intensity: int=Intensity.MEDIUM) -> None:
        super().__init__(name, intensity)

class StunnedEmotion(SurpriseEmotion):
    def __init__(self, name: str="Stunned", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class ShockedEmotion(StunnedEmotion):
    def __init__(self) -> None:
        super().__init__("Shocked", intensity=Intensity.SEVERAL)
class AstibusgedEmotion(StunnedEmotion):
    def __init__(self) -> None:
        super().__init__("Astibusged", intensity=Intensity.SEVERAL)

class ConfusedEmotion(SurpriseEmotion):
    def __init__(self, name: str="Confused", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class DisillusionedEmotion(ConfusedEmotion):
    def __init__(self) -> None:
        super().__init__("Disillusioned", intensity=Intensity.SEVERAL)
class PerplexEmotion(ConfusedEmotion):
    def __init__(self) -> None:
        super().__init__("Perplex", intensity=Intensity.SEVERAL)

class AmazedEmotion(SurpriseEmotion):
    def __init__(self, name: str="Amazed", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class AstonishedEmotion(AmazedEmotion):
    def __init__(self) -> None:
        super().__init__("Astonished", intensity=Intensity.SEVERAL)
class AweStruckEmotion(AmazedEmotion):
    def __init__(self) -> None:
        super().__init__("AweStruck", intensity=Intensity.SEVERAL)

class OvercomeEmotion(SurpriseEmotion):
    def __init__(self, name: str="Overcome", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class SpeechlessEmotion(OvercomeEmotion):
    def __init__(self) -> None:
        super().__init__("Speechless", intensity=Intensity.SEVERAL)
class AstoundedEmotion(OvercomeEmotion):
    def __init__(self) -> None:
        super().__init__("Astounded", intensity=Intensity.SEVERAL)

class MovedEmotion(SurpriseEmotion):
    def __init__(self, name: str="Moved", intensity: int=Intensity.HIGH) -> None:
        super().__init__(name, intensity)
class StimulatedEmotion(MovedEmotion):
    def __init__(self) -> None:
        super().__init__("Stimulated", intensity=Intensity.SEVERAL)
class TouchedEmotion(MovedEmotion):
    def __init__(self) -> None:
        super().__init__("Touched", intensity=Intensity.SEVERAL)

class EmotionsTree(metaclass=Singleton):
    def __init__(self) -> None:
        self.__emotions: dict[Emotion, dict[Emotion, list[Emotion]]] = {}
        fear: dict[Emotion, list[Emotion]] = {}
        fear[ScaredEmotion()] = [FrightenedEmotion(), HelplessEmotion()]
        fear[TerrorEmotion()] = [HystericalEmotion(), PanicEmotion()]
        fear[InsecureEmotion()] = [InadequateEmotion(), InferiorEmotion()]
        fear[NervousEmotion()] = [AnxiousEmotion(), WorriedEmotion()]
        fear[HorrorEmotion()] = [DreadEmotion(), MortifiedEmotion()]
        self.__emotions[FearEmotion()] = fear

        love: dict[Emotion, list[Emotion]] = {}
        love[PeacefulEmotion()] = [SatisfiedEmotion(), RelievedEmotion()]
        love[TendernessEmotion()] = [CompassionateEmotion(), CaringEmotion()]
        love[DesireEmotion()] = [InfaturationEmotion(), PassionEmotion()]
        love[LongingEmotion()] = [AttractedEmotion(), SentimentalEmotion()]
        love[AffectionnateEmotion()] = [FondnessEmotion(), RomanticEmotion()]
        self.__emotions[LoveEmotion()] = love

        joy: dict[Emotion, list[Emotion]] = {}
        joy[EnthralledEmotion()] = [RaptureEmotion(), EnchantedEmotion()]
        joy[ElationEmotion()] = [JubilationEmotion(), EuphoricEmotion()]
        joy[EnthusiasticEmotion()] = [ZealEmotion(), ExcitedEmotion()]
        joy[OptimisticEmotion()] = [HopefulEmotion(), EagerEmotion()]
        joy[ProudEmotion()] = [IllustriousEmotion(), TriumphantEmotion()]
        joy[CheerfulEmotion()] = [BlissfulEmotion(), JovialEmotion()]
        joy[HappyEmotion()] = [DelightedEmotion(), AmusedEmotion()]
        joy[ContentEmotion()] = [PleasedEmotion(), VerySatisfiedEmotion()]
        self.__emotions[JoyEmotion()] = joy

        anger: dict[Emotion, list[Emotion]] = {}
        anger[RageEmotion()] = [HateEmotion(), HostileEmotion()]
        anger[ExasperatedEmotion()] = [AgitatedEmotion(), FrustratedEmotion()]
        anger[IrritableEmotion()] = [AnnoyedEmotion(), AggravatedEmotion()]
        anger[EnvyEmotion()] = [ResentfulEmotion(), JealousEmotion()]
        anger[DisgustEmotion()] = [ContemptEmotion(), RevoltedEmotion()]
        self.__emotions[AngerEmotion()] = anger

        sadness: dict[Emotion, list[Emotion]] = {}
        sadness[SufferingEmotion()] = [AgonyEmotion(), HurtEmotion()]
        sadness[VerySadnessEmotion()] = [DepressedEmotion(), SorrowEmotion()]
        sadness[DisappointedEmotion()] = [DismayedEmotion(), DispleasedEmotion()]
        sadness[ShamefulEmotion()] = [RegretfulEmotion(), GuityEmotion()]
        sadness[NeglectedEmotion()] = [IsolatedEmotion(), LonelyEmotion()]
        sadness[DespairEmotion()] = [GriefEmotion(), PowerlessEmotion()]
        self.__emotions[SadnessEmotion()] = sadness

        surprise: dict[Emotion, list[Emotion]] = {}
        surprise[StunnedEmotion()] = [ShockedEmotion(), AstibusgedEmotion()]
        surprise[ConfusedEmotion()] = [DisillusionedEmotion(), PerplexEmotion()]
        surprise[AmazedEmotion()] = [AstonishedEmotion(), AweStruckEmotion()]
        surprise[OvercomeEmotion()] = [SpeechlessEmotion(), AstoundedEmotion()]
        surprise[MovedEmotion()] = [StimulatedEmotion(), TouchedEmotion()]
        self.__emotions[SurpriseEmotion()] = surprise

    @property
    def fear(self) -> dict[FearEmotion, list[FearEmotion]]:
        return self.__emotions.get(FearEmotion())
    @property
    def love(self) -> dict[LoveEmotion, list[LoveEmotion]]:
        return self.__emotions.get(LoveEmotion())
    @property
    def joy(self) -> dict[JoyEmotion, list[JoyEmotion]]:
        return self.__emotions.get(JoyEmotion())
    @property
    def anger(self) -> dict[AngerEmotion, list[AngerEmotion]]:
        return self.__emotions.get(AngerEmotion())
    @property
    def sadness(self) -> dict[SadnessEmotion, list[SadnessEmotion]]:
        return self.__emotions.get(SadnessEmotion())
    @property
    def surprise(self) -> dict[SurpriseEmotion, list[SurpriseEmotion]]:
        return self.__emotions.get(SurpriseEmotion())

    def get(self, emotion: Emotion) -> list[Emotion]:
        if (emotion in list(self.__emotions.keys())):
            return list(self.__emotions.get(emotion).keys())
        else:
            for primary_emotion in list(self.__emotions.keys()):
                if(emotion in list(self.__emotions.get(primary_emotion).keys())):
                    return self.__emotions.get(primary_emotion).get(emotion)
        return []

class EmotionalBeing:
    def __init__(self) -> None:
        self.__emotion: DefaultEmotion = NeutralEmotion()
    @property
    def emotion(self) -> DefaultEmotion:
        return self.__emotion

    def feel_fear(self):
        self.__emotion = FearEmotion()
    def feel_love(self):
        self.__emotion = LoveEmotion()
    def feel_joy(self):
        self.__emotion = JoyEmotion()
    def feel_anger(self):
        self.__emotion = AngerEmotion()
    def feel_sadness(self):
        self.__emotion = SadnessEmotion()
    def feel_surprise(self):
        self.__emotion = SurpriseEmotion()
    def feel_normal(self):
        self.__emotion = NeutralEmotion()
    def increase_intenisty(self):
        self.__emotion = self.__emotion.increase_intensity()
    def decrease_intenisty(self):
        self.__emotion = self.__emotion.decrease_intensity()
