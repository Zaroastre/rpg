package io.nirahtech.rpg.characters.inventories;

import java.util.List;

public interface Inventory {
    List<Slot<?>> getSlots();
}
