package io.nirahtech.videogame.tile;

import java.awt.Point;
import java.awt.image.BufferedImage;

import io.nirahtech.videogame.Entity;

public class Tile extends Entity {
    private final BufferedImage image;

    protected Tile(final BufferedImage image) {
        super(new Point(), new Point());
        this.image = image;
    }

    public BufferedImage getImage() {
        return image;
    }

    @Override
    public String toString() {
        return String.format("%s: %s", this.hashCode(), super.isCollision());
    }
}
