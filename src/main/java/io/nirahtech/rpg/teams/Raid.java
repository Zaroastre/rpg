package io.nirahtech.rpg.teams;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

import io.nirahtech.rpg.characters.Character;

public final class Raid implements Team {
    private final List<Group> groups = new ArrayList<>();

    @Override
    public Collection<Character> getMembers() {
        return Collections.unmodifiableCollection(
            this.groups.stream().flatMap(group -> group.getMembers().stream()).toList()
        );
    }

    public Collection<Group> getGroups() {
        return Collections.unmodifiableCollection(this.groups);
    }

    @Override
    public boolean add(Character character) {
        boolean isAdded = false;
        Objects.requireNonNull(character, "Character to add cannot be null");
        if (!this.getMembers().contains(character)) {
            for (Group group : this.groups) {
                isAdded = group.add(character);
                if (isAdded) {
                    character.invite(this);
                    break;
                }
            }
        }
        return isAdded;
        
    }

    @Override
    public boolean expel(Character character) {
        boolean isExpeled = false;
        Objects.requireNonNull(character, "Character to expel cannot be null");
        if (this.getMembers().contains(character)) {
            for (Group group : this.groups) {
                group.expel(character);
                character.expel(this);
            }
        }
        return isExpeled;
    }
}
