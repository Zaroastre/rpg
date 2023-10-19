package io.nirahtech.rpg.teams;

import java.util.Collection;

import io.nirahtech.rpg.characters.Character;

public interface Team {
    boolean add(Character character);
    boolean expel(Character character);
    Collection<Character> getMembers();
}
