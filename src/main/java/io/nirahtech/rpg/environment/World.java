package io.nirahtech.rpg.environment;

import java.util.Collection;

public record World (
    String name,
    Collection<Planet> planets
) {
    
}
