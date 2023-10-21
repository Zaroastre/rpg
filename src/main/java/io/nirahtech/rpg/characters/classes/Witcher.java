package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Adrenaline;
import io.nirahtech.rpg.characters.spells.DamageSpell;
import io.nirahtech.rpg.characters.spells.HealthSpell;
import io.nirahtech.rpg.characters.spells.InfectSpell;

/**
 * Witcher
 */
public final class Witcher extends AbstractCharacterClass implements SpellDamager, SpellCurser, Heal {
    public Witcher() {
        super(new Adrenaline());
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
}