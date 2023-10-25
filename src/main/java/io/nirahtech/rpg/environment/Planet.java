package io.nirahtech.rpg.environment;

import java.util.Collection;

public final record Planet (
    String name,
    Collection<Continent> continents
) {
    
}
