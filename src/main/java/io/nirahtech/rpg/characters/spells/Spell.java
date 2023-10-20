package io.nirahtech.rpg.characters.spells;

import java.time.Duration;
import java.time.LocalDateTime;

import io.nirahtech.rpg.characters.resources.ResourceType;

public interface Spell {
    String getName();
    String getDescription();

    int getRank();
    
    Duration getCooldown();

    boolean canBeCasted();
    
    ResourceType getRequiredResource();
    int getResourceUsage();
    
    void cast();
    LocalDateTime getLastCastDateTime();
    SpellType getType();

}
