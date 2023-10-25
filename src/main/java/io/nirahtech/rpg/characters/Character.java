package io.nirahtech.rpg.characters;

import java.io.File;

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
import io.nirahtech.rpg.characters.money.Currency;
import io.nirahtech.rpg.characters.races.Breed;
import io.nirahtech.rpg.characters.skiils.SkillsTree;
import io.nirahtech.rpg.characters.stuff.Wardrobe;
import io.nirahtech.rpg.weapons.Weapon;

public interface Character<T extends CharacterClass> extends Attack, Defend, Movable, Groupable, Targetable, Evolve, Threatable {
    String getName();
    Breed getBreed();
    T getCharacterClass();
    Weapon getWeapon();
    SkillsTree getSkillsTree();
    Inventory getInventory();
    Life getLife();
    Faction getFaction();
    HitBox getHitBox();
<<<<<<< HEAD
    Wardrobe getWardrobe();
    Body getBody();
=======
    Gender getGender();
    Currency getCurrency();
    File getAvatarPicture();
>>>>>>> 7093937391065b1d1207799095eb0e9954e6cd33
}
