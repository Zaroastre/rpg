package io.nirahtech.rpg.characters.races;

import java.util.Set;

import io.nirahtech.rpg.characters.abilities.RacialAbility;

public interface Breed {
    String getRaceName();
    int getBaseHealth();
    int getBaseResource();
    Set<RacialAbility> getRacialAbilities();
}
