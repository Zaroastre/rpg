package io.nirahtech.drivers.gamepad;

import java.util.Objects;

public class Joystick implements JoystickEventListener {

    private final Button button;
    private Position position;

    private Runnable onTiltCallback;

    public void setOnTiltCallback(Runnable onTiltCallback) {
        this.onTiltCallback = onTiltCallback;
    }

    public Joystick() {
        this(null);
        this.position = new Position(0, 0);
    }

    public Joystick(final Button button) {
        this.button = button;
    }

    @Override
    public void tilt(final Position position) {
        this.position = position;
        if (Objects.nonNull(this.onTiltCallback)) {
            this.onTiltCallback.run();
        }
    }

    public Position getPosition() {
        return position;
    }

}
