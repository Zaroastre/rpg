package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.spells.HealthSpell;

public interface Heal {
    void heal(HealthSpell spell, Character ally);
}
