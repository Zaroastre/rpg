package io.nirahtech.rpg.characters.resources;

public interface Resource {
    int getMaximumPoints();
    int getPoints();

    void increase(final int resourcePoints);
    void decrease(final int resourcePoints);
    
}
