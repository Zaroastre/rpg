package io.nirahtech.rpg.characters.actions;

public interface Evolve {
    int getLevel();
    int getMaximalExperience();
    int getCurrentExperience();
    void levelUp();
    void resetCurrentExperience();
}
