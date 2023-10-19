package io.nirahtech.rpg.characters.races;

import java.util.Set;

import io.nirahtech.rpg.characters.abilities.RacialAbility;

abstract class AbstractBreed implements Breed {

    @Override
    public int getBaseHealth() {
        // TODO Auto-generated method stub
        return 0;
    }

    @Override
    public int getBaseResource() {
        // TODO Auto-generated method stub
        return 0;
    }

    @Override
    public String getRaceName() {
        return this.getClass().getSimpleName();
    }

    @Override
    public Set<RacialAbility> getRacialAbilities() {
        // TODO Auto-generated method stub
        return null;
    }
    
}
