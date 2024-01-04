from rpg.artificial_intelligency.ai import ArtificialIntelligence

class ArtificialIntelligencyRegistry:
    def __init__(self) -> None:
        self.sentinel_ai: ArtificialIntelligence|None = None
    