package io.nirahtech.rpg.runtime.camera;

import io.nirahtech.rpg.characters.Character;

interface Tracker {
    void track(Character<?> characterToTrack);
    void untrack();
}
