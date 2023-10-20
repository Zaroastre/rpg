package io.nirahtech.rpg.characters;

import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.inventories.Bag;
import io.nirahtech.rpg.characters.races.Breed;

public final class CharacterFactory {
    private CharacterFactory() { }

    public static final Character create(final String name, final Breed breed, final CharacterClass characterClass, final Level level) {
        return new CharacterImpl(
            name,
            breed,
            characterClass,
            level,
            new Life(100),
            new Bag(5)
        );
    }
}
