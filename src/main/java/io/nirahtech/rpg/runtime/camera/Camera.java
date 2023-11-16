package io.nirahtech.rpg.runtime.camera;

import io.nirahtech.geometry.Point;
import io.nirahtech.rpg.characters.Character;

public class Camera implements Zoomable, Moveable, Tracker {

    private static final float MINIMAL_ZOOM = 0.0F;
    private static final float MAXIMAL_ZOOM = 100.0F;
    private static final float ZOOM_GAP = 10.0F;
    private static final float DEFAULT_ZOOM = 50.0F;

    private Point position;
    private float zoom = DEFAULT_ZOOM;
    private Character<?> characterToFollow = null;

    private int opticalWidth;
    private int opticalHeight;



    public Camera(final Point position) {
        this.position = position;
    }

    @Override
    public void moveBottom(int moveSpeed) {
        this.position = new Point(this.position.x(), this.position.y() + moveSpeed, this.position.z());
    }

    @Override
    public void moveTop(int moveSpeed) {
        this.position = new Point(this.position.x(), this.position.y() - moveSpeed, this.position.z());
    }

    @Override
    public void moveLeft(int moveSpeed) {
        this.position = new Point(this.position.x() - moveSpeed, this.position.y(), this.position.z());
    }

    @Override
    public void moveRight(int moveSpeed) {
        this.position = new Point(this.position.x() + moveSpeed, this.position.y(), this.position.z());
    }

    @Override
    public void zoomIn() {
        if ((this.zoom + ZOOM_GAP) <= MAXIMAL_ZOOM) {
            this.zoom += ZOOM_GAP;
        }
    }

    @Override
    public void zoomOut() {
        if ((this.zoom - ZOOM_GAP) <= MINIMAL_ZOOM) {
            this.zoom -= ZOOM_GAP;
        }
    }

    @Override
    public void resetZoom() {
        this.zoom = DEFAULT_ZOOM;
    }

    @Override
    public void track(Character<?> characterToTrack) {
        this.characterToFollow = characterToTrack;
    }
    @Override
    public void untrack() {
        this.characterToFollow = null;
    }
    
}
