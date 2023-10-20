package io.nirahtech.rpg.characters;

public final class Life {
    private int maximumPoints;
    private int points;

    public Life(final int points) {
        this(points, points);
    }

    public Life(final int points, final int maximumPoints) {
        this.points = points;
        this.maximumPoints = maximumPoints;
    }

    public int getPoints() {
        return this.points;
    }

    public int getMaximumPoints() {
        return this.maximumPoints;
    }

    public final boolean isAlive() {
        return this.points > 0;
    }
    public final boolean isDead() {
        return !this.isAlive();
    }

    public final void health(final int points) {
        this.points += points;
        if (this.points > this.maximumPoints) {
            this.points = this.maximumPoints;
        }
    }

    public final void loose(final int points) {
        this.points -= points;
    }

    public final void winBoost(final int lifePointsBoot) {
        this.maximumPoints += lifePointsBoot;
        this.points += lifePointsBoot;
    }
    
    public final void looseBoost(final int lifePointsBoot) {
        this.maximumPoints -= lifePointsBoot;
        if (this.points > this.maximumPoints) {
            this.points = this.maximumPoints;
        }
    }

}
