package io.nirahtech.rpg.characters;

import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.races.Breed;
import io.nirahtech.rpg.weapons.Weapon;

public final class CharacterBuilder {
    public CharacterBuilder() {

    }

    public final CharacterBuilder level(final int level) {
        return this;
    }

    public final CharacterBuilder breed(final Breed breed) {
        return this;
    }

    public final CharacterBuilder characterClass(final CharacterClass characterClass) {
        return this;
    }

    public final CharacterBuilder name(final String name) {
        return this;
    }

    public final CharacterBuilder weapon(final Weapon weapon) {
        return this;
    }

    

    public final Character<? extends CharacterClass> build() {
        return null;
    }
}
