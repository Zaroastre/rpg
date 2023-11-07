package io.nirahtech.rpg.interfaces.gui;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import io.nirahtech.drivers.InputDevice;
import io.nirahtech.rpg.interfaces.UserInterface;
import io.nirahtech.rpg.interfaces.gui.components.RpgWindow;

public final class GraphicalUserInterface implements UserInterface {

    private final Set<InputDevice> devices = new HashSet<>();

    @Override
    public void run(Map<String, Object> configuration) {
        final RpgWindow window = new RpgWindow();
        window.display();
    }

    @Override
    public void addInputDevice(InputDevice device) {
        this.devices.add(device);
    }
    
}
