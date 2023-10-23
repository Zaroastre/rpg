package io.nirahtech.rpg.characters.classes;

import java.util.Set;

import io.nirahtech.rpg.characters.resources.Energy;
import io.nirahtech.rpg.characters.roles.Role;

public final class Thieft extends AbstractCharacterClass {
    
    public Thieft() {
        super(ClassType.THIEFT, new Energy());
        super.roles.addAll(Set.of(Role.DPS));
    }
}
