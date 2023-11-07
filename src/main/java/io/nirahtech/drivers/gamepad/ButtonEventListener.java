package io.nirahtech.drivers.gamepad;

interface ButtonEventListener {
    void onPress();
    void onRelease();
    boolean isPressed();
}
