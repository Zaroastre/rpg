package io.nirahtech.rpg;

import java.util.HashMap;
import java.util.Map;

import io.nirahtech.drivers.gamepad.Gamepad;
import io.nirahtech.drivers.gamepad.Gamepads;
import io.nirahtech.drivers.keyboard.Keyboard;
import io.nirahtech.rpg.interfaces.UserInterface;
import io.nirahtech.rpg.interfaces.cli.CommandLineInterface;
import io.nirahtech.rpg.runtime.camera.Camera;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        final Map<String, Object> configuration = new HashMap<>();
        final UserInterface userInterface = new CommandLineInterface();
        userInterface.run(configuration);

        final Camera camera = new Camera(null);

        // camera.track(nicolas);

        final Gamepad gamepad = Gamepads.get();
        final Keyboard keyboard = new Keyboard();
        userInterface.addInputDevice(gamepad);
        userInterface.addInputDevice(keyboard);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            gamepad.shutdown();
        }));

        gamepad.onPressA(() -> {
            System.out.println("A pressed");
        });


    }
}
