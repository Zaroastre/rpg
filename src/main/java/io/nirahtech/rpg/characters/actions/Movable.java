package io.nirahtech.rpg.characters.actions;

import io.nirahtech.rpg.infrastructure.Point;

public interface Movable {
    void run();
    void walk();
    void jump();
    void squat();
    void getUp();
    void lieDown();
    Point getPosition();
}
