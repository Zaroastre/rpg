package io.nirahtech.rpg.characters.inventories;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

public class Bag implements Inventory {

    private final Map<?, Slot<?>> slots = new HashMap<>();

    public Bag(final int size) {

    }

    @Override
    public Collection<Slot<Object>> getSlots() {
        return null;
    }

    @Override
    public void put(Object object) {
        
    }

    @Override
    public void remove(Object object) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'remove'");
    }
    
}
