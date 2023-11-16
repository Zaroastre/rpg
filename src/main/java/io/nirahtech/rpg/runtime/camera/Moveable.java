package io.nirahtech.rpg.runtime.camera;

interface Moveable {
    void moveBottom(int moveSpeed);
    void moveTop(int moveSpeed);
    void moveLeft(int moveSpeed);
    void moveRight(int moveSpeed);
}
