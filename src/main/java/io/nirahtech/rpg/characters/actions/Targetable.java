package io.nirahtech.rpg.characters.actions;

import java.util.Optional;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;

public interface Targetable {
    void focus(Character<? extends CharacterClass> target);
    void releaseFocus(Character<? extends CharacterClass> target);
    Optional<Character<? extends CharacterClass>> getFocus();
}
