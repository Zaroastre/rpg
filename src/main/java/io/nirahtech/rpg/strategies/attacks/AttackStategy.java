package io.nirahtech.rpg.strategies.attacks;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;

public sealed interface AttackStategy permits SpellAttackStrategy, WeaponAttackStrategy {
    void attack(Character<? extends CharacterClass> target);
}
