package io.nirahtech.rpg.interfaces.gui;

import java.util.Map;

import io.nirahtech.rpg.interfaces.UserInterface;
import io.nirahtech.rpg.interfaces.gui.components.RpgWindow;

public final class GraphicalUserInterface implements UserInterface {

    @Override
    public void run(Map<String, Object> configuration) {
        final RpgWindow window = new RpgWindow();
        window.display();
    }
    
}
