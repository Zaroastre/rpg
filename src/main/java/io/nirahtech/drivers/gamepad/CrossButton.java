package io.nirahtech.drivers.gamepad;

public class CrossButton {
    private final Button top;
    private final Button left;
    private final Button bottom;
    private final Button right;

    public CrossButton() {
        this.top = new Button("CT");
        this.left = new Button("CL");
        this.bottom = new Button("CB");
        this.right = new Button("CR");
    }
}
