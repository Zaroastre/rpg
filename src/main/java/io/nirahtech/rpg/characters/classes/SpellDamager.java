package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.spells.DamageSpell;

interface SpellDamager {
    void cast(DamageSpell spell, Character enenmy);
}
