package io.nirahtech.rpg.strategies.attacks;

import io.nirahtech.rpg.characters.Character;

public sealed interface AttackStategy permits SpellAttackStrategy, WeaponAttackStrategy {
    void attack(Character target);
}
