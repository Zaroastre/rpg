package io.nirahtech.rpg.characters.classes;

import java.util.Set;

import io.nirahtech.rpg.characters.resources.Rage;
import io.nirahtech.rpg.characters.roles.Role;

public final class Warrior extends AbstractCharacterClass {
    
    public Warrior() {
        super(ClassType.WARRIOR, new Rage());
        super.roles.addAll(Set.of(Role.TANK, Role.DPS));
    }
}
