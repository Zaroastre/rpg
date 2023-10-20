package io.nirahtech.rpg.characters.resources;

public enum ResourceType {
    ADRENALINE(Adrenaline.class),
    ENERGY(Energy.class),
    MANA(Mana.class),
    QI(Qi.class),
    RAGE(Rage.class),
    ;

    private final Class<? extends Resource> classOfTheResource;

    private ResourceType(Class<? extends Resource> classOfTheResource) {
        this.classOfTheResource = classOfTheResource;
    }

    public Class<? extends Resource> getClassOfTheResource() {
        return classOfTheResource;
    }
}
