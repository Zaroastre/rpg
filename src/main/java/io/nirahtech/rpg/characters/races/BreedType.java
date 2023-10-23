package io.nirahtech.rpg.characters.races;

public enum BreedType {
    BLOOD_ELF(BloodElf.class),
    DWARD(Dwarf.class),
    GNOME(Gnome.class),
    HUMAN(Human.class),
    NIGHT_ELF(NightElf.class),
    ORC(Orc.class),
    TAUREN(Tauren.class),
    TROLL(Troll.class),
    UNDEAD(Undead.class),
    WORGEN(Worgen.class),
    ;

    private final Class<? extends Breed> breedClass;
    
    private BreedType(final Class<? extends Breed> breedClass) {
        this.breedClass = breedClass;
    }

    public Class<? extends Breed> getBreedClass() {
        return breedClass;
    }
}
