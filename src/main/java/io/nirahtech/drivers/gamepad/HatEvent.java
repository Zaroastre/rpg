package io.nirahtech.drivers.gamepad;

import io.nirahtech.drivers.Event;

public record HatEvent (
    int x,
    int y
)  implements Event {
    
}
