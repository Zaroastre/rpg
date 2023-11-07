package io.nirahtech.rpg.interfaces;

import java.util.Map;

import io.nirahtech.drivers.InputDevice;

public interface UserInterface {
    void run(Map<String, Object> configuration);

    void addInputDevice(InputDevice device);
}
