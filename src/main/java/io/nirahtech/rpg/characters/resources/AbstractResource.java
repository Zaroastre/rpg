package io.nirahtech.rpg.characters.resources;

abstract class AbstractResource implements Resource {
    private int points;
    private int maximumPoints;

    protected AbstractResource(final int points, final int maximumPoints) {
        this.points = points;
        this.maximumPoints = maximumPoints;
    }
    

    @Override
    public int getMaximumPoints() {
        return this.maximumPoints;
    }

    @Override
    public int getPoints() {
        return this.points;
    }

    @Override
    public void decrease(int resourcePoints) {
        this.points -= resourcePoints;
        if (this.points < 0) {
            this.points = 0;
        }
    }
    @Override
    public void increase(int resourcePoints) {
        this.points += resourcePoints;
        
        if (this.points > this.maximumPoints) {
            this.points = this.maximumPoints;
        }
    }
}
