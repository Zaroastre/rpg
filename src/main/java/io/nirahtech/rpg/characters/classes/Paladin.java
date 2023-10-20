package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.resources.Mana;

public final class Paladin extends AbstractCharacterClass {
    
    public Paladin() {
        super(new Mana(200, 200));
    }
}
