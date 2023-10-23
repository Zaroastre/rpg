package io.nirahtech.rpg.characters.stuff;

import java.util.Optional;

public final class GearSet {
    private final String name;

    private Stuff head;
    private Stuff leftShoulder;
    private Stuff leftArm;
    private Stuff leftHand;
    private Stuff rightShoulder;
    private Stuff rightArm;
    private Stuff rightHand;
    private Stuff torso;
    private Stuff back;
    private Stuff belt;
    private Stuff bottom;
    private Stuff leftKnee;
    private Stuff rightKnee;
    private Stuff foot;

    public GearSet(final String name) {
        this.name = name;
    }

    public final String getName() {
        return this.name;
    }

    public void setBack(Stuff back) {
        this.back = back;
    }
    public void setBelt(Stuff belt) {
        this.belt = belt;
    }
    public void setBottom(Stuff bottom) {
        this.bottom = bottom;
    }
    public void setFoot(Stuff foot) {
        this.foot = foot;
    }
    public void setHead(Stuff head) {
        this.head = head;
    }
    public void setLeftArm(Stuff leftArm) {
        this.leftArm = leftArm;
    }
    public void setLeftHand(Stuff leftHand) {
        this.leftHand = leftHand;
    }
    public void setLeftKnee(Stuff leftKnee) {
        this.leftKnee = leftKnee;
    }
    public void setLeftShoulder(Stuff leftShoulder) {
        this.leftShoulder = leftShoulder;
    }
    public void setRightArm(Stuff rightArm) {
        this.rightArm = rightArm;
    }
    public void setRightHand(Stuff rightHand) {
        this.rightHand = rightHand;
    }
    public void setRightKnee(Stuff rightKnee) {
        this.rightKnee = rightKnee;
    }
    public void setRightShoulder(Stuff rightShoulder) {
        this.rightShoulder = rightShoulder;
    }
    public void setTorso(Stuff torso) {
        this.torso = torso;
    }
    public Optional<Stuff> getBack() {
        return Optional.ofNullable(this.back);
    }
    
    public Optional<Stuff> getBelt() {
        return Optional.ofNullable(this.belt);
    }
    
    public Optional<Stuff> getBottom() {
        return Optional.ofNullable(this.bottom);
    }
    
    public Optional<Stuff> getFoot() {
        return Optional.ofNullable(this.foot);
    }
    
    public Optional<Stuff> getHead() {
        return Optional.ofNullable(this.head);
    }
    
    public Optional<Stuff> getLeftArm() {
        return Optional.ofNullable(this.leftArm);
    }
    
    public Optional<Stuff> getLeftHand() {
        return Optional.ofNullable(this.leftHand);
    }
    
    public Optional<Stuff> getLeftKnee() {
        return Optional.ofNullable(this.leftKnee);
    }
    
    public Optional<Stuff> getLeftShoulder() {
        return Optional.ofNullable(this.leftShoulder);
    }
    
    public Optional<Stuff> getRightArm() {
        return Optional.ofNullable(this.rightArm);
    }
    
    public Optional<Stuff> getRightHand() {
        return Optional.ofNullable(this.rightHand);
    }
    
    public Optional<Stuff> getRightKnee() {
        return Optional.ofNullable(this.rightKnee);
    }
    
    public Optional<Stuff> getTorso() {
        return Optional.ofNullable(this.torso);
    }
    public Optional<Stuff> getRightShoulder() {
        return Optional.ofNullable(this.rightShoulder);
    }

}
