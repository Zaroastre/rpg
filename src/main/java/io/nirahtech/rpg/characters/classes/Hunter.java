package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.resources.Mana;

public final class Hunter extends AbstractCharacterClass {
    
    public Hunter() {
        super(new Mana(200, 200));
    }
}
