package io.nirahtech.drivers.gamepad;

import java.util.Objects;

import io.nirahtech.drivers.Driver;
import io.nirahtech.drivers.InputDevice;

public final class Gamepad implements GamepadEventListerner, InputDevice<GamepadEvent> {
    private final Driver driver;

    private final Button a;
    private final Button b;
    private final Button x;
    private final Button y;

    private final Button rt;
    private final Button rb;

    private final Button lt;
    private final Button lb;

    private final Button start;
    private final Button select;

    private final Joystick leftStick;
    private final Joystick rightStick;

    private final CrossButton cross;

    Gamepad(final Driver driver) {
        this.driver = driver;
        if (Objects.nonNull(this.driver)) {
            this.driver.start();
        }
        this.a = new Button("A");
        this.b = new Button("B");
        this.x = new Button("X");
        this.y = new Button("Y");

        this.rt = new Button("RT");
        this.rb = new Button("RB");
        this.lt = new Button("LT");
        this.lb = new Button("LB");

        this.start = new Button("START");
        this.select = new Button("SELECT");

        this.leftStick = new Joystick(new Button("LS"));
        this.rightStick = new Joystick(new Button("RS"));

        this.cross = new CrossButton();
        this.driver.setController(this);
    }

    @Override
    public void onPressLB(Runnable callback) {
        this.lb.setOnPressCallback(() -> {
            callback.run();
        });
    }

    @Override
    public void onReleaseLB(Runnable callback) {
        this.lb.setOnReleaseCallback(() -> {
            callback.run();
        });
    }

    @Override
    public void onPressLT(Runnable callback) {
        this.lt.setOnPressCallback(() -> {
            callback.run();
        });
    }

    @Override
    public void onReleaseLT(Runnable callback) {
        this.lt.setOnReleaseCallback(() -> {
            callback.run();
        });
    }

    @Override
    public void onPressRB(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressRB'");
    }

    @Override
    public void onReleaseRB(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseRB'");
    }

    @Override
    public void onPressRT(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressRT'");
    }

    @Override
    public void onReleaseRT(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseRT'");
    }

    @Override
    public void onPressA(Runnable callback) {
        this.a.setOnPressCallback(callback);
    }

    @Override
    public void onReleaseA(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseA'");
    }

    @Override
    public void onPressB(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressB'");
    }

    @Override
    public void onReleaseB(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseB'");
    }

    @Override
    public void onPressX(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressX'");
    }

    @Override
    public void onReleaseX(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseX'");
    }

    @Override
    public void onPressY(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressY'");
    }

    @Override
    public void onReleaseY(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseY'");
    }

    @Override
    public void onPressCrossLeft(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressCrossLeft'");
    }

    @Override
    public void onReleaseCrossLeft(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseCrossLeft'");
    }

    @Override
    public void onPressCrossTop(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressCrossTop'");
    }

    @Override
    public void onReleaseCrossTop(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseCrossTop'");
    }

    @Override
    public void onPressCrossRight(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressCrossRight'");
    }

    @Override
    public void onReleaseCrossRight(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseCrossRight'");
    }

    @Override
    public void onPressCrossBottom(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressCrossBottom'");
    }

    @Override
    public void onReleaseCrossBottom(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseCrossBottom'");
    }

    @Override
    public void onPressLeftStick(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressLeftStick'");
    }

    @Override
    public void onReleaseLeftStick(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseLeftStick'");
    }

    @Override
    public void onPressRightStick(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onPressRightStick'");
    }

    @Override
    public void onReleaseRightStick(Runnable callback) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'onReleaseRightStick'");
    }

    @Override
    public void handle(GamepadEvent event) {
        switch (event.button()) {
            case BUTTON_A:
                if (((ButtonEvent) event.eventValue()).isPressed()) {
                    this.a.onPress();
                } else {
                    this.a.onRelease();
                }
                break;

            case BUTTON_B:
                if (((ButtonEvent) event.eventValue()).isPressed()) {
                    this.b.onPress();
                } else {
                    this.b.onRelease();
                }
                break;
            case BUTTON_X:
                if (((ButtonEvent) event.eventValue()).isPressed()) {
                    this.x.onPress();
                } else {
                    this.x.onRelease();
                }
                break;

                case BUTTON_Y:
                if (((ButtonEvent) event.eventValue()).isPressed()) {
                    this.y.onPress();
                } else {
                    this.y.onRelease();
                }
                break;
        
            default:
                break;
        }

    }

    public void shutdown() {
        this.driver.stop();
    }

}
