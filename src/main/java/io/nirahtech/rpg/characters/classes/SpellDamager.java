package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.spells.DamageSpell;

public interface SpellDamager {
    void cast(DamageSpell spell, Character<? extends CharacterClass> enenmy);
}
