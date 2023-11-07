package io.nirahtech.drivers.gamepad;

import java.util.Objects;

public final class Button implements ButtonEventListener {
    private final String name;
    private boolean isPressed = false;

    private Runnable onPressCallback;
    private Runnable onReleaseCallback;

    public Button(final String name) {
        this.name = name;
    }

    public void setOnPressCallback(final Runnable onPressCallback) {
        this.onPressCallback = onPressCallback;
    }

    public void setOnReleaseCallback(final Runnable onReleaseCallback) {
        this.onReleaseCallback = onReleaseCallback;
    }

    public String getName() {
        return name;
    }

    @Override
    public void onPress() {
        this.isPressed = true;
        if (Objects.nonNull(this.onPressCallback)) {
            this.onPressCallback.run();
        }
    }

    @Override
    public void onRelease() {
        this.isPressed = false;
        if (Objects.nonNull(this.onReleaseCallback)) {
            this.onReleaseCallback.run();
        }
    }

    @Override
    public boolean isPressed() {
        return this.isPressed;
    }
    
}
