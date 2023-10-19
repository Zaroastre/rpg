package io.nirahtech.rpg.characters.actions;

import io.nirahtech.rpg.teams.Group;
import io.nirahtech.rpg.teams.Raid;

public interface Groupable {
    void invite(Group group);
    void expel(Group group);
    void invite(Raid raid);
    void expel(Raid raid);
}
