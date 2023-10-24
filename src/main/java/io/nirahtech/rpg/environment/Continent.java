package io.nirahtech.rpg.environment;

import java.util.Collection;

public final record Continent (
    String name,
    Collection<Region> regions
) {
    
}
