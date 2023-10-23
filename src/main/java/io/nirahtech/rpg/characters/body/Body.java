package io.nirahtech.rpg.characters.body;

import io.nirahtech.rpg.characters.Life;

public final class Body {
    private final Head head;
    private final Neck neck;

    private final Shoulder leftShoulder;
    private final SuperiorArm leftArm;

    private final Shoulder rightShoulder;
    private final SuperiorArm rightArm;

    private final Torso torso;
    private final Back back;
    private final Waist waist;

    public Body() {
        this.head = new Head(new Life(20));
        this.neck = new Neck(new Life(10));
        this.leftShoulder = new LeftShoulder(new Life(5));
        this.rightShoulder = new RightShoulder(new Life(5));
        this.leftArm = new SuperiorArm(new LeftForeArm(new Life(10)), new LeftElbow(new Life(5)),
                new LeftArm(new Life(10)), new LeftHand(new Life(6)));
        this.rightArm = new SuperiorArm(new RightForeArm(new Life(10)), new RightElbow(new Life(5)),
                new RightArm(new Life(10)), new RightHand(new Life(6)));
        this.torso = new Torso(new Life(25));
        this.back = new Back(new Life(15));
        this.waist = new Waist(new Life(10));
    }

    public Head getHead() {
        return head;
    }

    public SuperiorArm getLeftArm() {
        return leftArm;
    }

    public Shoulder getLeftShoulder() {
        return leftShoulder;
    }

    public Neck getNeck() {
        return neck;
    }

    public SuperiorArm getRightArm() {
        return rightArm;
    }

    public Shoulder getRightShoulder() {
        return rightShoulder;
    }

    public Back getBack() {
        return back;
    }

    public Torso getTorso() {
        return torso;
    }

    public Waist getWaist() {
        return waist;
    }

    public int getMaximumLifePoints() {
        int totalLifePoints = 0;
        totalLifePoints += head.getLife().getMaximumPoints();
        totalLifePoints += neck.getLife().getMaximumPoints();
        totalLifePoints += leftShoulder.getLife().getMaximumPoints();
        totalLifePoints += rightShoulder.getLife().getMaximumPoints();
        totalLifePoints += leftArm.getMaximumLifePoints();
        totalLifePoints += rightArm.getMaximumLifePoints();
        totalLifePoints += torso.getLife().getMaximumPoints();
        totalLifePoints += back.getLife().getMaximumPoints();
        totalLifePoints += waist.getLife().getMaximumPoints();
        return totalLifePoints;

    }

    public int getCurrentLifePoints() {
        int totalCurrentLifePoints = 0;
        totalCurrentLifePoints += head.getLife().getPoints();
        totalCurrentLifePoints += neck.getLife().getPoints();
        totalCurrentLifePoints += leftShoulder.getLife().getPoints();
        totalCurrentLifePoints += rightShoulder.getLife().getPoints();
        totalCurrentLifePoints += leftArm.getCurrentLifePoints();
        totalCurrentLifePoints += rightArm.getCurrentLifePoints();
        totalCurrentLifePoints += torso.getLife().getPoints();
        totalCurrentLifePoints += back.getLife().getPoints();
        totalCurrentLifePoints += waist.getLife().getPoints();
        return totalCurrentLifePoints;

    }

}
