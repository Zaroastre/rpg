package io.nirahtech.rpg.characters;

import java.util.HashMap;
import java.util.Map;

public final class Level {
    private int value;
    private long currentExperience;
    private long requiredExperienceToAchieveTheLevel;

    private Level(final int value, final long requiredExperienceToAchieveTheLevel) {
        this.value = value;
        this.requiredExperienceToAchieveTheLevel = requiredExperienceToAchieveTheLevel;
        this.currentExperience = 0;
    }

    public final int getValue() {
        return value;
    }
    public final long getCurrentExperience() {
        return currentExperience;
    }
    public final long getRequiredExperienceToAchieveTheLevel() {
        return requiredExperienceToAchieveTheLevel;
    }

    public final void winExperience(final int experience) {
        this.currentExperience += experience;
        if (this.currentExperience >= this.requiredExperienceToAchieveTheLevel) {
            this.up();
        }
    }
    
    public final void up() {
        this.value ++;
        this.currentExperience = 0;
    }
    
    public static final class Factory {
        private static final Map<Integer, Long> AVAILABLE_LEVELS = new HashMap<>();
        private static final int TOTAL_AVAILABLE_LEVELS = 20;
        private static final float EXPERIENCE_DELTA_BETWEEN_LEVELS = 1.5F;
        private Factory() { }

        private static final void initializeLevels() {
            if (AVAILABLE_LEVELS.isEmpty()) {
                long requiredExperience = 100L;

                for (int level = 1; level <= TOTAL_AVAILABLE_LEVELS; level++) {
                    AVAILABLE_LEVELS.put(level, requiredExperience);
                    requiredExperience *= Math.round(level * EXPERIENCE_DELTA_BETWEEN_LEVELS);
                }
            }
        }

        public static final Level create(final int level) {
            initializeLevels();
            return new Level(level, AVAILABLE_LEVELS.getOrDefault(level, 100_000L));
        }
    }
}
