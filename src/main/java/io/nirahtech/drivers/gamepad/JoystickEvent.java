package io.nirahtech.drivers.gamepad;

import io.nirahtech.drivers.Event;

public record JoystickEvent(
    float value
) implements Event {
    
}
