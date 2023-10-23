package io.nirahtech.rpg.characters.actions;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.infrastructure.Point;

public interface Movable {

    void goTo(Point point);

    void stayInPlace();
    void walk();
    void run();
    void sprint();

    void jump();
    void squat();
    void getUp();
    void lieDown();
    
    Point getPosition();

    void follow(Character<? extends CharacterClass> target);

    boolean isMoving();
}
