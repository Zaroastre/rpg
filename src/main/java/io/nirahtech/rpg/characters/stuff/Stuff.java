package io.nirahtech.rpg.characters.stuff;

import java.util.Map;
import java.util.Set;

import io.nirahtech.rpg.characters.StatisticType;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.races.Breed;

public interface Stuff {
    String getName();
    String getDescription();
    int getRequiredMinimalLevel();
    Rarity getRarity();
    
    Set<CharacterClass> getRequiredClasses();
    Set<Breed> getRequiredBreeds();
    Map<StatisticType, Float> getStatistics();
}
