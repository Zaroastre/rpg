package io.nirahtech.rpg.weapons;

import io.nirahtech.rpg.characters.Character;

public interface Weapon {
    String getName();
    String getDescription();
    int getMinimalDamage();
    int getMaximalDamage();
    float getSpeed();
    float getHitChance();
    int damage(Character target);
}
