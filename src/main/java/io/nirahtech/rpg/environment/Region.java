package io.nirahtech.rpg.environment;

import java.util.Collection;
import java.util.Map;

import io.nirahtech.rpg.infrastructure.Point;
import io.nirahtech.rpg.teams.Raid;

public final record Region (
    String name,
    int minimalRecommendedLevel,
    int maximalRecommendedLevel,
    Collection<City> cities,
    Map<Point, Raid> enemies
) {
    
}
