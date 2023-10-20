package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Mana;
import io.nirahtech.rpg.characters.spells.Spell;

public final class Demonist extends AbstractCharacterClass implements SpellDamager {

    public Demonist() {
        super(new Mana(200, 200));
    }

    @Override
    public void cast(Spell spell, Character target) {
        spell.cast(target);
    }
}
