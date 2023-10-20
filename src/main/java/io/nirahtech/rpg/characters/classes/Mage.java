package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.resources.Mana;

public final class Mage extends AbstractCharacterClass {
    
    public Mage() {
        super(new Mana(200, 200));
    }
}
