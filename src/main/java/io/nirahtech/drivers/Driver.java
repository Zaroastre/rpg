package io.nirahtech.drivers;

public interface Driver {
    void start();
    void stop();
    void handle(Event event);
    void setController(InputDevice device);
}
