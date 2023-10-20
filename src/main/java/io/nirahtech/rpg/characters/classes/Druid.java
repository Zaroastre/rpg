package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Mana;
import io.nirahtech.rpg.characters.spells.Spell;

public final class Druid extends AbstractCharacterClass implements SpellDamager {
    
    public Druid() {
        super(new Mana(200, 200));
    }

    @Override
    public void cast(Spell spell, Character target) {
        spell.cast(target);
    }
}
