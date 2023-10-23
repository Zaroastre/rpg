package io.nirahtech.rpg.interfaces.cli;

import java.util.Map;

import io.nirahtech.rpg.interfaces.UserInterface;
import io.nirahtech.rpg.interfaces.gui.GraphicalUserInterface;

public class CommandLineInterface implements UserInterface {

    @Override
    public void run(Map<String, Object> configuration) {
        final UserInterface gui = new GraphicalUserInterface();
        gui.run(configuration);
    }
    
}
