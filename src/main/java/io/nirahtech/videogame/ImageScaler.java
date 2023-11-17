package io.nirahtech.videogame;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;

public final class ImageScaler {

    private ImageScaler() { }

    /**
     * Resize an image.
     * @param originalImage Image to resize.
     * @param width New width.
     * @param height New height.
     * @return New resized image.
     */
    public static final BufferedImage scaleImage(final BufferedImage originalImage, final int width, final int height) {
        final BufferedImage scaledImage = new BufferedImage(width, height, originalImage.getType());
        final Graphics2D graphics = scaledImage.createGraphics();
        graphics.drawImage(originalImage, 0, 0, width, height, null);
        graphics.dispose();
        return scaledImage;
    }
}
