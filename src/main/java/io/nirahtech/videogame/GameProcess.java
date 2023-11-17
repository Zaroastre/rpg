package io.nirahtech.videogame;

import java.awt.Graphics;

public interface GameProcess {

    /**
     * In this first step, event handling and computation are processed.
     */
    void update();

    /**
     * In this second step, graphics are updated while painting screen.
     * 
     * @param graphics The graphic context where draw.
     */
    void paintComponent(final Graphics graphics);
}
