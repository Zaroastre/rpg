package io.nirahtech.drivers.gamepad;

interface GamepadEventListerner {
    void onPressLB(Runnable eventCallback);
    void onReleaseLB(Runnable eventCallback);

    void onPressLT(Runnable eventCallback);
    void onReleaseLT(Runnable eventCallback);

    void onPressRB(Runnable eventCallback);
    void onReleaseRB(Runnable eventCallback);

    void onPressRT(Runnable eventCallback);
    void onReleaseRT(Runnable eventCallback);

    void onPressA(Runnable eventCallback);
    void onReleaseA(Runnable eventCallback);

    void onPressB(Runnable eventCallback);
    void onReleaseB(Runnable eventCallback);

    void onPressX(Runnable eventCallback);
    void onReleaseX(Runnable eventCallback);

    void onPressY(Runnable eventCallback);
    void onReleaseY(Runnable eventCallback);

    void onPressCrossLeft(Runnable eventCallback);
    void onReleaseCrossLeft(Runnable eventCallback);

    void onPressCrossTop(Runnable eventCallback);
    void onReleaseCrossTop(Runnable eventCallback);

    void onPressCrossRight(Runnable eventCallback);
    void onReleaseCrossRight(Runnable eventCallback);

    void onPressCrossBottom(Runnable eventCallback);
    void onReleaseCrossBottom(Runnable eventCallback);

    void onPressLeftStick(Runnable eventCallback);
    void onReleaseLeftStick(Runnable eventCallback);

    void onPressRightStick(Runnable eventCallback);
    void onReleaseRightStick(Runnable eventCallback);

}
