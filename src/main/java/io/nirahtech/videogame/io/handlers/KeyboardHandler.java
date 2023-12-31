package io.nirahtech.videogame.io.handlers;

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ResourceBundle;
import java.util.logging.Logger;

import io.nirahtech.rpg.interfaces.gui.components.GamePanel;
import io.nirahtech.videogame.Initializable;
import io.nirahtech.videogame.enumerations.GameStep;

public final class KeyboardHandler implements KeyListener, Initializable {
    private static final Logger LOGGER = Logger.getLogger(KeyboardHandler.class.getSimpleName());
    private static KeyboardHandler instance;
    private GamePanel gamePanel = null;
    private boolean isLocked = false;

    public static final KeyboardHandler getInstance() {
        LOGGER.info("Calling unique instance of keyboard handler");
        if (KeyboardHandler.instance == null) {
            KeyboardHandler.instance = new KeyboardHandler();
        }
        return KeyboardHandler.instance;
    }

    private KeyboardHandler() {

    }

    private boolean upPressed, downPressed, leftPressed, rightPressed, enterPressed, shiftPressed = false;

    public boolean isUpPressed() {
        return upPressed;
    }

    public boolean isDownPressed() {
        return downPressed;
    }

    public boolean isLeftPressed() {
        return leftPressed;
    }

    public boolean isRightPressed() {
        return rightPressed;
    }

    public boolean isEnterPressed() {
        return this.enterPressed;
    }

    public boolean isShiftPressed() {
        return shiftPressed;
    }

    @Override
    public void keyTyped(KeyEvent event) {

        // TODO Auto-generated method stub

    }


    public boolean isLocked() {
        return isLocked;
    }

    @Override
    public void keyPressed(KeyEvent event) {
        if (this.gamePanel.getGameStep() == GameStep.MAIN_MENU) {
            if (!this.isLocked) {
                switch (event.getKeyCode()) {
                    case KeyEvent.VK_Z:
                    case KeyEvent.VK_UP:
                        this.upPressed = true;
                        this.isLocked = true;
                        break;
                    case KeyEvent.VK_S:
                    case KeyEvent.VK_DOWN:
                        this.downPressed = true;
                        this.isLocked = true;
                        break;
                    case KeyEvent.VK_ENTER:
                        this.enterPressed = true;
                        this.isLocked = true;
                        break;
                }
            }
        } else if (this.gamePanel.getGameStep() == GameStep.IN_GAME) {
            switch (event.getKeyCode()) {
                case KeyEvent.VK_Z:
                case KeyEvent.VK_UP:
                    this.upPressed = true;
                    break;
                case KeyEvent.VK_S:
                case KeyEvent.VK_DOWN:
                    this.downPressed = true;
                    break;
                case KeyEvent.VK_Q:
                case KeyEvent.VK_LEFT:
                    this.leftPressed = true;
                    break;
                case KeyEvent.VK_D:
                case KeyEvent.VK_RIGHT:
                    this.rightPressed = true;
                    break;
                case KeyEvent.VK_SHIFT:
                    this.shiftPressed = true;
                    break;
                case KeyEvent.VK_P:
                    if (this.gamePanel.getGameStep() == GameStep.IN_GAME) {
                        this.gamePanel.setGameStep(GameStep.PAUSED);
                    } else if (this.gamePanel.getGameStep() == GameStep.PAUSED) {
                        this.gamePanel.setGameStep(GameStep.IN_GAME);
                    }
                    break;
                case KeyEvent.VK_M:
                    this.gamePanel.getSound().stop();
                    break;
                default:
                    break;
            }

        }
    }

    @Override
    public void keyReleased(KeyEvent event) {
        if (this.gamePanel.getGameStep() == GameStep.MAIN_MENU) {
            this.isLocked = false;

            switch (event.getKeyCode()) {
                case KeyEvent.VK_Z:
                case KeyEvent.VK_UP:
                    this.upPressed = false;
                    break;
                case KeyEvent.VK_S:
                case KeyEvent.VK_DOWN:
                    this.downPressed = false;
                    this.isLocked = false;
                    break;
                case KeyEvent.VK_ENTER:
                    this.enterPressed = false;
                    this.isLocked = false;
                    break;

            }
        } else if (this.gamePanel.getGameStep() == GameStep.IN_GAME) {
            switch (event.getKeyCode()) {
                case KeyEvent.VK_Z:
                case KeyEvent.VK_UP:
                    this.upPressed = false;
                    break;
                case KeyEvent.VK_S:
                case KeyEvent.VK_DOWN:
                    this.downPressed = false;
                    break;
                case KeyEvent.VK_Q:
                case KeyEvent.VK_LEFT:
                    this.leftPressed = false;
                    break;
                case KeyEvent.VK_D:
                case KeyEvent.VK_RIGHT:
                    this.rightPressed = false;
                    break;
                case KeyEvent.VK_SHIFT:
                    this.shiftPressed = false;
                    break;
                default:
                    break;
            }
        }
    }

    @Override
    public void initialize(ResourceBundle configuration) {
        LOGGER.info("Initializing keyboard key handler instance...");
        this.gamePanel = GamePanel.getInstance();
        LOGGER.info("Keyboard key handler instance initialized.");
    }
}
