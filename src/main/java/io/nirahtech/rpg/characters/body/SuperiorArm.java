package io.nirahtech.rpg.characters.body;

public final class SuperiorArm extends AbstractBodyPart {
    private final ForeArm foreArm;
    private final Elbow elbow;
    private final Arm arm;
    private final Hand hand;

    public SuperiorArm(
        final ForeArm foreArm,
        final Elbow elbow,
        final Arm arm,
        final Hand hand
    ) {
        super(null);
        this.foreArm = foreArm;
        this.elbow = elbow;
        this.arm = arm;
        this.hand = hand;
    }

    public Arm getArm() {
        return arm;
    }
    public Elbow getElbow() {
        return elbow;
    }
    public ForeArm getForeArm() {
        return foreArm;
    }
    public Hand getHand() {
        return hand;
    }

    
    public int getMaximumLifePoints() {
        int totalLifePoints = 0;
        totalLifePoints += foreArm.getLife().getMaximumPoints();
        totalLifePoints += elbow.getLife().getMaximumPoints();
        totalLifePoints += arm.getLife().getMaximumPoints();
        totalLifePoints += hand.getLife().getMaximumPoints();
        return totalLifePoints;

    }

    public int getCurrentLifePoints() {
        int totalCurrentLifePoints = 0;
        totalCurrentLifePoints += foreArm.getLife().getPoints();
        totalCurrentLifePoints += elbow.getLife().getPoints();
        totalCurrentLifePoints += arm.getLife().getPoints();
        totalCurrentLifePoints += hand.getLife().getPoints();
        return totalCurrentLifePoints;

    }
}
