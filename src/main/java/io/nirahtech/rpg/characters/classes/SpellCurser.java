package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.spells.InfectSpell;

public interface SpellCurser {
    
    void curse(InfectSpell spell, Character enemy);
}
