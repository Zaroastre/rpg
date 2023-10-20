package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.resources.Mana;

public final class Shaman extends AbstractCharacterClass {
    
    public Shaman() {
        super(new Mana(200, 200));
    }
}
