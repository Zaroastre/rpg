package io.nirahtech.rpg.strategies.attacks;

import java.util.Objects;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.spells.Spell;

public final class SpellAttackStrategy implements AttackStategy {
    private final Spell spell;
    
    public SpellAttackStrategy(final Spell spell) {
        this.spell = spell;
    }

    @Override
    public void attack(Character<? extends CharacterClass> target) {
        if (Objects.nonNull(this.spell) && Objects.nonNull(target)) {
            this.spell.cast(target);
        }
    }
    
}
