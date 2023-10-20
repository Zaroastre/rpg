package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.resources.Mana;

public final class Priest extends AbstractCharacterClass {
    
    public Priest() {
        super(new Mana(200, 200));
    }
}
