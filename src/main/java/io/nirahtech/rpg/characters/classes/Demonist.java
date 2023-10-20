package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.resources.Mana;

public final class Demonist extends AbstractCharacterClass {

    public Demonist() {
        super(new Mana(200, 200));
    }
    
}
