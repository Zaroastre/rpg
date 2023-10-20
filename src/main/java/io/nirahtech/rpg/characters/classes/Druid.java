package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.resources.Mana;

public final class Druid extends AbstractCharacterClass {
    
    public Druid() {
        super(new Mana(200, 200));
    }
}
