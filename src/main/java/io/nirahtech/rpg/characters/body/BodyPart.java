package io.nirahtech.rpg.characters.body;

import java.util.Optional;

import io.nirahtech.rpg.characters.Life;
import io.nirahtech.rpg.characters.stuff.Stuff;

public interface BodyPart {
    Optional<Stuff> getStuff();
    void dress(Stuff stuff);
    Stuff undress();
    Life getLife();
}
