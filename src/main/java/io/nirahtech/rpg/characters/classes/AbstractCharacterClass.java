package io.nirahtech.rpg.characters.classes;

import java.util.Set;

import io.nirahtech.rpg.characters.abilities.ClassAbility;
import io.nirahtech.rpg.characters.skiils.SkillsTree;
import io.nirahtech.rpg.weapons.Weapon;

abstract class AbstractCharacterClass implements CharacterClass {
    @Override
    public String getClassName() {
        return this.getClass().getSimpleName();
    }
    
    @Override
    public int getBaseAttackDamage() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getBaseAttackDamage'");
    }

    @Override
    public int getBaseResourceDamage() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getBaseResourceDamage'");
    }

    @Override
    public Set<ClassAbility> getClassAbilities() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getClassAbilities'");
    }

    @Override
    public Weapon getPreferedWeapon() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getPreferedWeapon'");
    }
    @Override
    public SkillsTree getSkillsTree() {
        // TODO Auto-generated method stub
        return null;
    }
}
