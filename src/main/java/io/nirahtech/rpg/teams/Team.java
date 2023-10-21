package io.nirahtech.rpg.teams;

import java.util.Collection;

import io.nirahtech.rpg.characters.Character;

public sealed interface Team permits Group, Raid {
    boolean add(Character character);
    boolean expel(Character character);
    Collection<Character> getMembers();
}
