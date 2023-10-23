package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.spells.GuardianSpell;

public interface Guardian {
    void watchOver(GuardianSpell spell, Character<? extends CharacterClass> ally);
}
