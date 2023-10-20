package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Adrenaline;
import io.nirahtech.rpg.characters.spells.Spell;

/**
 * Witcher
 */
public final class Witcher extends AbstractCharacterClass implements SpellDamager {
    public Witcher() {
        super(new Adrenaline());
    }

    @Override
    public void cast(Spell spell, Character target) {
        spell.cast(target);
    }
}