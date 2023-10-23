package io.nirahtech.rpg.characters.classes;

import java.util.HashSet;
import java.util.Set;

import io.nirahtech.rpg.characters.abilities.ClassAbility;
import io.nirahtech.rpg.characters.resources.Resource;
import io.nirahtech.rpg.characters.roles.Role;
import io.nirahtech.rpg.characters.skiils.SkillsTree;
import io.nirahtech.rpg.weapons.Weapon;

abstract class AbstractCharacterClass implements CharacterClass {

    private final Resource resource;
    private final ClassType classType;
    protected final Set<Role> roles = new HashSet<>();

    protected AbstractCharacterClass(final ClassType classType, final Resource resource) {
        this.classType = classType;
        this.resource = resource;
    }

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

    @Override
    public Resource getResource() {
        return this.resource;
    }

    @Override
    public ClassType getClassType() {
        return this.classType;
    }

    @Override
    public Set<Role> getRoles() {
        return this.roles;
    }
}
