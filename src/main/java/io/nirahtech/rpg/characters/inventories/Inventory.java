package io.nirahtech.rpg.characters.inventories;

import java.util.Collection;

public interface Inventory {
    Collection<Slot<Object>> getSlots();

    void put(Object object);
    void remove(Object object);
}
