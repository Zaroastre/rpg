package io.nirahtech.rpg.characters.classes;

import io.nirahtech.rpg.characters.Factory;

public enum ClassType implements Factory<CharacterClass> {
    DEMONIST(Demonist.class) {
        @Override
        public CharacterClass create() {
            return new Demonist();
        }
    },
    DRUID(Druid.class) {
        @Override
        public CharacterClass create() {
            return new Druid();
        }
    },
    HUNTER(Hunter.class) {
        @Override
        public CharacterClass create() {
            return new Hunter();
        }
    },
    MAGE(Mage.class) {
        @Override
        public CharacterClass create() {
            return new Mage();
        }
    },
    MONK(Monk.class) {
        @Override
        public CharacterClass create() {
            return new Monk();
        }
    },
    PALADIN(Paladin.class) {
        @Override
        public CharacterClass create() {
            return new Paladin();
        }
    },
    PRIEST(Priest.class) {
        @Override
        public CharacterClass create() {
            return new Priest();
        }
    },
    SHAMAN(Shaman.class) {
        @Override
        public CharacterClass create() {
            return new Shaman();
        }
    },
    THIEFT(Thieft.class) {
        @Override
        public CharacterClass create() {
            return new Thieft();
        }
    },
    WARRIOR(Warrior.class) {
        @Override
        public CharacterClass create() {
            return new Warrior();
        }
    },
    WITCHER(Witcher.class) {
        @Override
        public CharacterClass create() {
            return new Witcher();
        }
    };

    private final Class<? extends CharacterClass> characterClass;
    private ClassType(final Class<? extends CharacterClass> characterClass) {
        this.characterClass = characterClass;
    }

    public Class<? extends CharacterClass> getCharacterClass() {
        return characterClass;
    }
}
