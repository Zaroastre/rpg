package io.nirahtech.rpg.teams;

import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;

public final class Group implements Team {

    private final Character<? extends CharacterClass>[] members;

    private Group(final int size) {
        this.members = new Character[size];
    }

    @Override
    public final Collection<Character<? extends CharacterClass>> getMembers() {
        return Collections.unmodifiableSet(new HashSet<>(Arrays.asList(this.members)));
    }

    @Override
    public final boolean add(final Character<? extends CharacterClass> character) {
        boolean isAdded = false;
        Objects.requireNonNull(character, "Character<? extends CharacterClass> to add cannot be null");
        final Set<Character> existingmembers = new HashSet<>(Arrays.asList(this.members));
        if (!existingmembers.contains(character)) {
            for (int index = 0; index < this.members.length; index++) {
                if (Objects.isNull(this.members[index])) {
                    this.members[index] = character;
                    isAdded = true;
                    character.invite(this);
                }
            }
        }
        return isAdded;
    }

    @Override
    public final boolean expel(final Character<? extends CharacterClass> character) {
        boolean isExpeled = false;
        Objects.requireNonNull(character, "Character<? extends CharacterClass> to expel cannot be null");
        final Set<Character> existingmembers = new HashSet<>(Arrays.asList(this.members));
        if (existingmembers.contains(character)) {   
            for (int index = 0; index < this.members.length; index++) {
                if (this.members[index] == character) {
                    this.members[index] = null;
                    isExpeled = true;
                    character.expel(this);
                }
            }
        }
        return isExpeled;
    }

    public static final Group create(final int size) {
        return new Group(size);
    }
}
