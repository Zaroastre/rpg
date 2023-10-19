package io.nirahtech.rpg.characters;

import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.races.Breed;

public final class CharacterFactory {
    private CharacterFactory() { }

    public static final Character create(final Breed breed, final CharacterClass characterClass) {
        return new CharacterImpl();
    }
}
