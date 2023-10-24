package io.nirahtech.rpg.environment;

import java.util.Collection;

import io.nirahtech.rpg.teams.Raid;

public final record Region (
    String name,
    int minimalRecommendedLevel,
    int maximalRecommendedLevel,
    Collection<City> cities,
    Collection<Raid> mobs
) {
    
}
