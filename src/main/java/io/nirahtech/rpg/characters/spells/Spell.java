package io.nirahtech.rpg.characters.spells;

import java.time.Duration;
import java.time.LocalDateTime;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.resources.ResourceType;

public interface Spell {
    String getName();
    String getDescription();

    int getRank();
    
    Duration getCooldown();
    Duration getInvantationDuration();

    boolean canBeCasted();
    
    ResourceType getRequiredResource();
    int getResourceUsage();
    
    void cast(Character<? extends CharacterClass> target);
    LocalDateTime getLastCastDateTime();
    SpellType getType();

}
