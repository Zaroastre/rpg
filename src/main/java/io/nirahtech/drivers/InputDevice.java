package io.nirahtech.drivers;

public interface InputDevice<T extends Event> {
    void handle(T event);
}
