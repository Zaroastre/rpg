package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.spells.Spell;

interface SpellDamager {
    void cast(Spell spell, Character target);
}
