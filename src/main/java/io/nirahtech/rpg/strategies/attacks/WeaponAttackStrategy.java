package io.nirahtech.rpg.strategies.attacks;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.weapons.Weapon;

public final class WeaponAttackStrategy implements AttackStategy {
    private final Weapon weapon;
    
    public WeaponAttackStrategy(final Weapon weapon) {
        this.weapon = weapon;
    }

    @Override
    public void attack(Character target) {
        this.weapon.damage(target);
    }
    
}
