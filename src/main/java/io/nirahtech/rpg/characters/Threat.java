package io.nirahtech.rpg.characters;

public class Threat {

    private static final int LOW_LEVEL_THRESHOLD = 30;
    private static final int MEDIUM_LEVEL_THRESHOLD = 60;
    private static final int HIGH_LEVEL_THRESHOLD = 90;

    private int level = 0;

    public final int getLevel() {
        return this.level;
    }

    public void increase(final int points) {
        this.level += points;
    }
    public void decrease(final int points) {
        this.level -= points;
    }

    public void reset() {
        this.level = 0;
    }

    public final boolean isLow() {
        return this.level < LOW_LEVEL_THRESHOLD;
    }
    
    public final boolean isMedium() {
        return this.level < MEDIUM_LEVEL_THRESHOLD;
    }
    
    public final boolean isHigh() {
        return this.level < HIGH_LEVEL_THRESHOLD;
    }

    public final boolean isCritical() {
        return this.level >= HIGH_LEVEL_THRESHOLD;
    }

}
