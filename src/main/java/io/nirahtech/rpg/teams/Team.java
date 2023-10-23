package io.nirahtech.rpg.teams;

import java.util.Collection;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;

public sealed interface Team permits Group, Raid {
    boolean add(Character<? extends CharacterClass> character);
    boolean expel(Character<? extends CharacterClass> character);
    Collection<Character<? extends CharacterClass>> getMembers();
}
