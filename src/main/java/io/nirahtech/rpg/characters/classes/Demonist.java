package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Mana;
import io.nirahtech.rpg.characters.spells.DamageSpell;
import io.nirahtech.rpg.characters.spells.InfectSpell;

public final class Demonist extends AbstractCharacterClass implements SpellDamager, SpellCurser {

    public Demonist() {
        super(new Mana(200, 200));
    }

    @Override
    public void cast(DamageSpell spell, Character enemy) {
        spell.cast(enemy);
    }

    @Override
    public void curse(InfectSpell spell, Character enemy) {
        spell.cast(enemy);
        
    }
}
