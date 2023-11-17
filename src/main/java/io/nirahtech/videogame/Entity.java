package io.nirahtech.videogame;

import java.awt.Point;
import java.awt.Rectangle;

import io.nirahtech.rpg.interfaces.gui.components.GamePanel;
import io.nirahtech.videogame.apis.Collisionable;
import io.nirahtech.videogame.apis.GeoLocalizable;

public abstract class Entity implements Collisionable<Entity>, GeoLocalizable {

    protected static final GamePanel GAME_PANEL = GamePanel.getInstance();

    private boolean isCollision = false;
    protected final Point positionOnTheWorldMap;
    protected final Point positionOnTheScreen;
    protected final Point solidAreaDefaultLocation;
    protected final Rectangle solidArea;
    protected int animationSpeed = 2;

    protected Entity(Point mapLocation, Point screenLocation) {
        this.positionOnTheWorldMap = mapLocation;
        this.positionOnTheScreen = screenLocation;
        this.solidAreaDefaultLocation = new Point(this.positionOnTheScreen.x, this.positionOnTheScreen.y);
        this.solidArea = new Rectangle(
                this.solidAreaDefaultLocation.x,
                this.solidAreaDefaultLocation.y,
                GAME_PANEL.getTileSize(),
                GAME_PANEL.getTileSize());
    }

    @Override
    public void setCollision(boolean collision) {
        this.isCollision = collision;
    }

    @Override
    public boolean isCollision() {
        return this.isCollision;
    }

    @Override
    public boolean isInCollisionWith(Entity otherEntity) {
        return false;
    }

    @Override
    public Point getPositionOnTheWorldMap() {
        return this.positionOnTheWorldMap;
    }

    @Override
    public Point getPositionOnTheScreen() {
        return this.positionOnTheScreen;
    }

    @Override
    public Point getSolidAreaDefaultLocation() {
        return this.solidAreaDefaultLocation;
    }

    @Override
    public Rectangle getSolidArea() {
        return this.solidArea;
    }

}
