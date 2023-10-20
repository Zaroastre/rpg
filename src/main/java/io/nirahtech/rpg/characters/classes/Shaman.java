package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Mana;
import io.nirahtech.rpg.characters.spells.Spell;

public final class Shaman extends AbstractCharacterClass implements SpellDamager {
    
    public Shaman() {
        super(new Mana(200, 200));
    }

    @Override
    public void cast(Spell spell, Character target) {
        spell.cast(target);
    }
}
