package io.nirahtech.rpg.characters.classes;

import java.util.Set;

import io.nirahtech.rpg.characters.abilities.ClassAbility;
import io.nirahtech.rpg.characters.skiils.SkillsTree;
import io.nirahtech.rpg.weapons.Weapon;

public interface CharacterClass {
    String getClassName();
    int getBaseAttackDamage();
    int getBaseResourceDamage();
    Set<ClassAbility> getClassAbilities();
    Weapon getPreferedWeapon();
    SkillsTree getSkillsTree();
}
