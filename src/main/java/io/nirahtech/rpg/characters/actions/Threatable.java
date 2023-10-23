package io.nirahtech.rpg.characters.actions;

import java.util.Optional;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.Threat;
import io.nirahtech.rpg.characters.classes.CharacterClass;

public interface Threatable {
    Optional<Threat> getThreat(Character<? extends CharacterClass> target);
}
