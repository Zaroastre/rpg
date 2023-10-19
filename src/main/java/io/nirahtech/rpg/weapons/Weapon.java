package io.nirahtech.rpg.weapons;

public interface Weapon {
    String getName();
    String getDescription();
    int getMinimalDamage();
    int getMaximalDamage();
    float getSpeed();
    float getHitChance();
}
