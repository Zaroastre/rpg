package io.nirahtech.rpg.characters.body;

import java.util.Optional;

import io.nirahtech.rpg.characters.Life;
import io.nirahtech.rpg.characters.stuff.Stuff;

abstract class AbstractBodyPart implements BodyPart {
    private Stuff stuff;
    private final Life life;

    protected AbstractBodyPart(final Life life) {
        this.life = life;
    }

    @Override
    public final Optional<Stuff> getStuff() {
        return Optional.ofNullable(this.stuff);
    }

    @Override
    public final void dress(Stuff stuff) {
        this.stuff = stuff;
    }

    @Override
    public Stuff undress() {
        Stuff removedStuff = this.stuff;
        this.stuff = null;
        return removedStuff;
    }

    @Override
    public Life getLife() {
        return this.life;
    }
}
