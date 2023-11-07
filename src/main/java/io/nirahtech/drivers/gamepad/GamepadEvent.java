package io.nirahtech.drivers.gamepad;

import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import io.nirahtech.drivers.Event;

public record GamepadEvent(
        GamepadButtons button,
        Event eventValue) implements Event {

    private static final String BUTTON_REGEX = "<Event\\((1540|1539)-JoyButton(Up|Down) \\{'joy': \\d{1,}, 'instance_id': \\d{1,}, 'button': (\\d{1,})";    
    private static final String STICK_REGEX = "<Event\\(1536-JoyAxisMotion \\{'joy': \\d{1,}, 'instance_id': \\d{1,}, 'axis': (\\d{1,}), 'value': ((-)?([0|1](.)?\\d{1,}))";
    private static final String HAT_REGEX = "<Event\\(1538-JoyHatMotion \\{'joy': \\d{1,}, 'instance_id': \\d{1,}, 'hat': (\\d{1,}), 'value': \\(((-)?(0|1)), ((-)?(0|1))\\)";
 
    private static final Pattern BUTTON_PATTERN = Pattern.compile(BUTTON_REGEX);
    private static final Pattern STICK_PATTERN = Pattern.compile(STICK_REGEX);
    private static final Pattern HAT_PATTERN = Pattern.compile(HAT_REGEX);


    private static final GamepadEvent retrieveButtonEvent(final String rawEvent) {
        GamepadEvent event = null;
        final Matcher matcher = BUTTON_PATTERN.matcher(rawEvent);
        if (matcher.find()) {
            final boolean isPressed = Integer.parseInt(matcher.group(1)) == 1539;
            GamepadButtons button = null;
            final int buttonIdentifier = Integer.parseInt(matcher.group(3));
                switch (buttonIdentifier) {
                    case 0:
                        button = GamepadButtons.BUTTON_Y;
                        break;
                    case 1:
                        button = GamepadButtons.BUTTON_B;
                        break;
                    case 2:
                        button = GamepadButtons.BUTTON_A;
                        break;
                    case 3:
                        button = GamepadButtons.BUTTON_X;
                        break;
                    case 4:
                        button = GamepadButtons.BUTTON_LB;
                        break;
                    case 5:
                        button = GamepadButtons.BUTTON_RB;
                        break;
                    case 6:
                        button = GamepadButtons.BUTTON_LT;
                        break;
                    case 7:
                        button = GamepadButtons.BUTTON_RT;
                        break;
                    case 8:
                        button = GamepadButtons.BUTTON_SELECT;
                        break;
                    case 9:
                        button = GamepadButtons.BUTTON_START;
                        break;
                    case 10:
                        button = GamepadButtons.STICK_LEFT_BUTTON;
                        break;
                    case 11:
                        button = GamepadButtons.STICK_RIGHT_BUTTON;
                        break;
                    default:
                        break;
                }
                if (Objects.nonNull(button)) {
                    event = new GamepadEvent(button, new ButtonEvent(isPressed, !isPressed));
                }
        }
        return event;
    }

    private static final GamepadEvent retrieveStickEvent(final String rawEvent) {
        GamepadEvent event = null;
        final Matcher matcher = STICK_PATTERN.matcher(rawEvent);
        if (matcher.find()) {
            final int axe = Integer.parseInt(matcher.group(1));
            final float tilt = Float.parseFloat(matcher.group(2));
            GamepadButtons button = null;
            switch (axe) {
                case 0:
                    button = GamepadButtons.STICK_LEFT_MOTION_X;
                    break;
                case 1:
                button = GamepadButtons.STICK_LEFT_MOTION_Y;
                    break;
                    case 2:
                        button = GamepadButtons.STICK_RIGHT_MOTION_X;
                        break;
                    case 3:
                    button = GamepadButtons.STICK_RIGHT_MOTION_Y;
                        break;
                    
            }
            event = new GamepadEvent(button, new JoystickEvent(tilt));
        }
        return event;
    }

    private static final GamepadEvent retrieveHatEvent(final String rawEvent) {
        GamepadEvent event = null;
        final Matcher matcher = HAT_PATTERN.matcher(rawEvent);        if (matcher.find()) {
            final int x = Integer.parseInt(matcher.group(2));
            final int y = Integer.parseInt(matcher.group(5));
            event = new GamepadEvent(GamepadButtons.BUTTON_CROSS, new HatEvent(x, y));
        }
        return event;
    }


    public static final GamepadEvent parse(final String rawEvent) {
        GamepadEvent event = null;
        event = retrieveButtonEvent(rawEvent);
        if (Objects.isNull(event)) {
            event = retrieveStickEvent(rawEvent);
        }
        if (Objects.isNull(event)) {
            event = retrieveHatEvent(rawEvent);
        }
        return event;
    }
}
