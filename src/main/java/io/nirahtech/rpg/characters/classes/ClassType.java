package io.nirahtech.rpg.characters.classes;

public enum ClassType {
    DEMONIST(Demonist.class),
    DRUID(Druid.class),
    HUNTER(Hunter.class),
    MAGE(Mage.class),
    MONK(Monk.class),
    PALADIN(Paladin.class),
    PRIEST(Priest.class),
    SHAMAN(Shaman.class),
    THIEFT(Thieft.class),
    WARRIOR(Warrior.class),
    WITCHER(Witcher.class);

    private final Class<? extends CharacterClass> characterClass;
    private ClassType(final Class<? extends CharacterClass> characterClass) {
        this.characterClass = characterClass;
    }

    public Class<? extends CharacterClass> getCharacterClass() {
        return characterClass;
    }
}
