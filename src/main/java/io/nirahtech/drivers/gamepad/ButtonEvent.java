package io.nirahtech.drivers.gamepad;

import io.nirahtech.drivers.Event;

public record ButtonEvent (
    boolean isPressed,
    boolean isReleased
) implements Event {
    
}
