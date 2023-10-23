package io.nirahtech.rpg.characters.classes;

import java.util.Set;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Mana;
import io.nirahtech.rpg.characters.roles.Role;
import io.nirahtech.rpg.characters.spells.DamageSpell;
import io.nirahtech.rpg.characters.spells.GuardianSpell;
import io.nirahtech.rpg.characters.spells.HealthSpell;
import io.nirahtech.rpg.characters.spells.InfectSpell;

public final class Shaman extends AbstractCharacterClass implements SpellDamager, SpellCurser, Heal, Guardian {
    
    public Shaman() {
        super(ClassType.SHAMAN, new Mana(200, 200));
        super.roles.addAll(Set.of(Role.TANK, Role.DPS, Role.HEAL));
    }

    @Override
    public void cast(DamageSpell spell, Character<? extends CharacterClass> enemy) {
        spell.cast(enemy);
    }

    @Override
    public void heal(HealthSpell spell, Character<? extends CharacterClass> ally) {
        spell.cast(ally);
    }
    @Override
    public void curse(InfectSpell spell, Character<? extends CharacterClass> enemy) {
        spell.cast(enemy);
    }
    @Override
    public void watchOver(GuardianSpell spell, Character<? extends CharacterClass> ally) {
        spell.cast(ally);
    }
}
