package io.nirahtech.rpg.characters;

import io.nirahtech.rpg.infrastructure.Point;

public final class HitBox {
    private Point center;
    private final int radius;

    public HitBox(final Point center, final int radius) {
        this.center = center;
        this.radius = radius;
    }

    public Point getCenter() {
        return center;
    }

    public float getRadius() {
        return radius;
    }

    public void setCenter(Point center) {
        this.center = center;
    }

    public final Point getLeft() {
        return new Point(this.center.x() - this.radius, this.center.y(), this.center.z());
    }

    public final Point getRight() {
        return new Point(this.center.x() + this.radius, this.center.y(), this.center.z());
    }

    public final Point getTop() {
        return new Point(this.center.x(), this.center.y() - this.radius, this.center.z());
    }

    public final Point getBottom() {
        return new Point(center.x(), this.center.y() + this.radius, this.center.z());
    }

    public final boolean collide(final HitBox hitBox) {
        // Calculez la distance entre les centres des deux hitboxes
        double distance = Math.sqrt(
                Math.pow(this.center.x() - hitBox.getCenter().x(), 2) +
                        Math.pow(this.center.y() - hitBox.getCenter().y(), 2));

        // Si la distance entre les centres est inférieure à la somme des rayons des
        // deux hitboxes, alors elles se chevauchent
        return distance < this.radius + hitBox.getRadius();
    }
}
