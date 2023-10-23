package io.nirahtech.rpg.characters.actions;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.strategies.attacks.AttackStategy;

public interface Attack {
    void attack(AttackStategy attackStategy, Character<? extends CharacterClass> target);
}
