package io.nirahtech.rpg.environment;

import java.awt.Point;
import java.util.Collection;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.Faction;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.teams.Raid;

public final record City (
    String name,
    Point location,
    Collection<Faction> factions,
    Character<? extends CharacterClass> chief,
    Raid army
) {
    
}
