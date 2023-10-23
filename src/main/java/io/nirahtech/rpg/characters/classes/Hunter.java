package io.nirahtech.rpg.characters.classes;

import java.util.Set;

import io.nirahtech.rpg.characters.resources.Mana;
import io.nirahtech.rpg.characters.roles.Role;

public final class Hunter extends AbstractCharacterClass {
    
    public Hunter() {
        super(ClassType.HUNTER, new Mana(200, 200));
        super.roles.addAll(Set.of(Role.DPS));
    }
}
