package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.resources.Qi;
import io.nirahtech.rpg.characters.spells.GuardianSpell;
import io.nirahtech.rpg.characters.spells.HealthSpell;

public final class Monk extends AbstractCharacterClass implements Heal, Guardian {
    
    public Monk() {
        super(new Qi());
    }
    
    @Override
    public void heal(HealthSpell spell, Character ally) {
        spell.cast(ally);
    }

    @Override
    public void watchOver(GuardianSpell spell, Character ally) {
        spell.cast(ally);
    }

}
