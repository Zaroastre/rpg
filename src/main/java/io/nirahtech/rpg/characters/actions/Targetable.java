package io.nirahtech.rpg.characters.actions;

import io.nirahtech.rpg.characters.Character;

import java.util.Optional;

public interface Targetable {
    void focus(Character target);
    void releaseFocus(Character target);
    Optional<io.nirahtech.rpg.characters.Character> getFocus();
}
