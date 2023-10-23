package io.nirahtech.rpg.weapons;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;

public interface Weapon {
    String getName();
    String getDescription();
    int getMinimalDamage();
    int getMaximalDamage();
    float getSpeed();
    float getHitChance();
    int damage(Character<? extends CharacterClass> target);
}
