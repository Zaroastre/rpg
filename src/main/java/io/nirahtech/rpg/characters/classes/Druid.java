package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Mana;
import io.nirahtech.rpg.characters.spells.DamageSpell;
import io.nirahtech.rpg.characters.spells.GuardianSpell;
import io.nirahtech.rpg.characters.spells.HealthSpell;
import io.nirahtech.rpg.characters.spells.InfectSpell;

public final class Druid extends AbstractCharacterClass implements SpellDamager, SpellCurser, Heal, Guardian {
    
    public Druid() {
        super(new Mana(200, 200));
    }

    @Override
    public void cast(DamageSpell spell, Character enemy) {
        spell.cast(enemy);
    }

    @Override
    public void heal(HealthSpell spell, Character ally) {
        spell.cast(ally);
    }

    @Override
    public void curse(InfectSpell spell, Character enemy) {
        spell.cast(enemy);
    }
    @Override
    public void watchOver(GuardianSpell spell, Character ally) {
        spell.cast(ally);
    }
}
