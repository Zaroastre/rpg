package io.nirahtech.drivers.gamepad;

public final class Gamepads {

    private Gamepads() { }

    public static final Gamepad get() {
        return new Gamepad(new GamepadDriver());
    } 
}
