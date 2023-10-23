package io.nirahtech.rpg.characters.classes;

import java.util.Set;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Mana;
import io.nirahtech.rpg.characters.roles.Role;
import io.nirahtech.rpg.characters.spells.DamageSpell;
import io.nirahtech.rpg.characters.spells.InfectSpell;

public final class Mage extends AbstractCharacterClass implements SpellDamager, SpellCurser {
    
    public Mage() {
        super(ClassType.MAGE, new Mana(200, 200));
        super.roles.addAll(Set.of(Role.DPS));
    }

    @Override
    public void cast(DamageSpell spell, Character<? extends CharacterClass> enemy) {
        spell.cast(enemy);
    }
    @Override
    public void curse(InfectSpell spell, Character<? extends CharacterClass> enemy) {
        spell.cast(enemy);
    }
}
