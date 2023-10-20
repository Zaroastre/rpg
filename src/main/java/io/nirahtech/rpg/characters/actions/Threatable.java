package io.nirahtech.rpg.characters.actions;

import java.util.Optional;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.Threat;

public interface Threatable {
    Optional<Threat> getThreat(Character target);
}
