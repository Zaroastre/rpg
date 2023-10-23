package io.nirahtech.rpg.characters.classes;

import java.util.Set;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Qi;
import io.nirahtech.rpg.characters.roles.Role;
import io.nirahtech.rpg.characters.spells.GuardianSpell;
import io.nirahtech.rpg.characters.spells.HealthSpell;

public final class Monk extends AbstractCharacterClass implements Heal, Guardian {
    
    public Monk() {
        super(ClassType.MONK, new Qi());
        super.roles.addAll(Set.of(Role.TANK, Role.DPS, Role.HEAL));
    }
    
    @Override
    public void heal(HealthSpell spell, Character<? extends CharacterClass> ally) {
        spell.cast(ally);
    }

    @Override
    public void watchOver(GuardianSpell spell, Character<? extends CharacterClass> ally) {
        spell.cast(ally);
    }

}
