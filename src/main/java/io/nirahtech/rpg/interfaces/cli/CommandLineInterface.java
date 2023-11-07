package io.nirahtech.rpg.interfaces.cli;

import java.util.Map;
import java.util.Objects;

import io.nirahtech.drivers.InputDevice;
import io.nirahtech.rpg.interfaces.UserInterface;
import io.nirahtech.rpg.interfaces.gui.GraphicalUserInterface;

public class CommandLineInterface implements UserInterface {
    private UserInterface gui = null;

    @Override
    public void run(Map<String, Object> configuration) {
        this.gui = new GraphicalUserInterface();
        this.gui.run(configuration);
    }

    @Override
    public void addInputDevice(InputDevice device) {
        if (Objects.nonNull(this.gui)) {
            this.gui.addInputDevice(device);
        }
        
    }
    
}
