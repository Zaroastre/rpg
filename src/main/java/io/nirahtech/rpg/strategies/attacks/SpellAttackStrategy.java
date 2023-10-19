package io.nirahtech.rpg.strategies.attacks;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.spells.Spell;

public final class SpellAttackStrategy implements AttackStategy {
    private final Spell spell;
    
    public SpellAttackStrategy(final Spell spell) {
        this.spell = spell;
    }

    @Override
    public void attack(Character target) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'attack'");
    }
    
}
