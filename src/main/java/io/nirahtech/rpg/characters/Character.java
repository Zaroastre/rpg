package io.nirahtech.rpg.characters;

import io.nirahtech.rpg.characters.actions.Attack;
import io.nirahtech.rpg.characters.actions.Defend;
import io.nirahtech.rpg.characters.actions.Evolve;
import io.nirahtech.rpg.characters.actions.Groupable;
import io.nirahtech.rpg.characters.actions.Movable;
import io.nirahtech.rpg.characters.actions.Targetable;
import io.nirahtech.rpg.characters.actions.Threatable;
import io.nirahtech.rpg.characters.body.Body;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.inventories.Inventory;
import io.nirahtech.rpg.characters.races.Breed;
import io.nirahtech.rpg.characters.skiils.SkillsTree;
import io.nirahtech.rpg.characters.stuff.Wardrobe;
import io.nirahtech.rpg.weapons.Weapon;

public interface Character<T extends CharacterClass> extends Attack, Defend, Movable, Groupable, Targetable, Evolve, Threatable {
    Breed getBreed();
    T getCharacterClass();
    Weapon getWeapon();
    SkillsTree getSkillsTree();
    Inventory getInventory();
    Life getLife();
    Faction getFaction();
    HitBox getHitBox();
    Wardrobe getWardrobe();
    Body getBody();
}
