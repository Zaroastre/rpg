package io.nirahtech.rpg.characters.races;

import io.nirahtech.rpg.characters.Factory;
import io.nirahtech.rpg.characters.classes.CharacterClass;

public enum BreedType implements Factory<Breed> {
    BLOOD_ELF(BloodElf.class) {
        @Override
        public Breed create() {
            return new BloodElf();
        }
    },
    DWARF(Dwarf.class) {
        @Override
        public Breed create() {
            return new Dwarf();
        }
    },
    GNOME(Gnome.class) {
        @Override
        public Breed create() {
            return new Gnome();
        }
    },
    HUMAN(Human.class) {
        @Override
        public Breed create() {
            return new Human();
        }
    },
    NIGHT_ELF(NightElf.class) {
        @Override
        public Breed create() {
            return new NightElf();
        }
    },
    ORC(Orc.class) {
        @Override
        public Breed create() {
            return new Orc();
        }
    },
    TAUREN(Tauren.class) {
        @Override
        public Breed create() {
            return new Tauren();
        }
    },
    TROLL(Troll.class) {
        @Override
        public Breed create() {
            return new Troll();
        }
    },
    UNDEAD(Undead.class) {
        @Override
        public Breed create() {
            return new Undead();
        }
    },
    WORGEN(Worgen.class) {
        @Override
        public Breed create() {
            return new Worgen();
        }
    },
    ;

    private final Class<? extends Breed> breedClass;
    
    private BreedType(final Class<? extends Breed> breedClass) {
        this.breedClass = breedClass;
    }

    public Class<? extends Breed> getBreedClass() {
        return breedClass;
    }
}
