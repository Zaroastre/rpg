package io.nirahtech.rpg.characters;

import java.io.File;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

import io.nirahtech.rpg.characters.body.Body;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.inventories.Inventory;
import io.nirahtech.rpg.characters.money.Currency;
import io.nirahtech.rpg.characters.races.Breed;
import io.nirahtech.rpg.characters.skiils.SkillsTree;
import io.nirahtech.rpg.characters.stuff.Wardrobe;
import io.nirahtech.rpg.infrastructure.Point;
import io.nirahtech.rpg.strategies.attacks.AttackStategy;
import io.nirahtech.rpg.teams.Group;
import io.nirahtech.rpg.teams.Raid;
import io.nirahtech.rpg.weapons.Weapon;

class CharacterImpl<T extends CharacterClass> implements Character<T> {

    private static final int CHARACTER_HITBOX_RADIUS = 10;

    private final String name;

    private final Breed breed;
    private final T characterClass;
    
    private final Faction faction;
    private final Level level;
    private final Life life;
    
    private final Inventory inventory;

    private final Wardrobe wardrobe;
    private final Map<Character<? extends CharacterClass>, Threat> threats = new HashMap<>();

    private final HitBox hitBox;
<<<<<<< HEAD
    private final Body body;
=======
    private final Gender gender;
    private final Currency currency;
>>>>>>> 7093937391065b1d1207799095eb0e9954e6cd33
    private float moveSpeed;

    private Character<? extends CharacterClass> target = null;
    private File avatarPicture;

    private Group group;
    private Raid raid;

    private Weapon weapon;
    private boolean isMoving = false;


    CharacterImpl(
        final String name,
        final Breed breed,
        final T characterClass,
        final Faction faction,
        final Gender gender,
        final Level level,
        final Life life,
        final Inventory inventory
    ) {
        this.name = name;
        this.breed = breed;
        this.faction = faction;
        this.characterClass = characterClass;
        this.level = level;
        this.life = life;
        this.inventory = inventory;
        this.wardrobe = new Wardrobe();
        this.life.winBoost(this.breed.getBaseHealth());
        this.hitBox = new HitBox(new Point(0, 0, 0), CHARACTER_HITBOX_RADIUS);
        this.body = new Body();
        this.moveSpeed = 1.1F;
        this.gender = gender;
        this.currency = new Currency(10, 0, 0);

    }

    @Override
    public void attack(AttackStategy attackStategy, Character<? extends CharacterClass> target) {
        attackStategy.attack(target);
    }

    @Override
    public void escape() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'escape'");
    }

    @Override
    public void wardOff() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'wardOff'");
    }

    @Override
    public void run() {
        this.isMoving = true;
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'run'");
    }

    @Override
    public void walk() {
        this.isMoving = true;
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'walk'");
    }

    @Override
    public void jump() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'jump'");
    }

    @Override
    public void squat() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'squat'");
    }

    @Override
    public void getUp() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getUp'");
    }

    @Override
    public void lieDown() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'lieDown'");
    }

    @Override
    public void invite(Group group) {
        this.group = group;
    }

    @Override
    public void expel(Group group) {
        if (this.group.equals(group)) {
            this.group = null;
        }
    }

    @Override
    public void invite(Raid raid) {
        if (Objects.nonNull(raid)) {
            if (Objects.nonNull(this.raid)) {
                this.raid.expel(this);
            }
            this.raid = raid;
            this.raid.add(this);
        }
    }

    @Override
    public void expel(Raid raid) {
        if (Objects.nonNull(this.raid) && this.raid.equals(raid)) {
            this.raid = null;
        }
    }

    @Override
    public void focus(Character<? extends CharacterClass> target) {
        this.target = target;
    }

    @Override
    public void releaseFocus(Character<? extends CharacterClass> target) {
        if (this.target.equals(target)) {
            this.target = null;
        }
    }

    @Override
    public Optional<Character<? extends CharacterClass>> getFocus() {
        return Optional.ofNullable(this.target);
    }

    @Override
    public Breed getBreed() {
        return this.breed;
    }

    @Override
    public T getCharacterClass() {
        return this.characterClass;
    }


    @Override
    public Weapon getWeapon() {
        return this.weapon;
    }

    @Override
    public SkillsTree getSkillsTree() {
        return this.getCharacterClass().getSkillsTree();
    }

    @Override
    public Inventory getInventory() {
        return this.inventory;
    }

    @Override
    public Point getPosition() {
        return this.hitBox.getCenter();
    }

    @Override
    public Optional<Threat> getThreat(Character<? extends CharacterClass> target) {
        return Optional.ofNullable(this.threats.get(target));
    }

    @Override
    public Level getLevel() {
        return this.level;
    }

    @Override
    public Life getLife() {
        return this.life;
    }

    @Override
    public Faction getFaction() {
        return this.faction;
    }

    @Override
    public void follow(Character<? extends CharacterClass> target) {
        // TODO [NME] Must be implemented.
    }

    @Override
    public void sprint() {
        this.isMoving = true;
    }

    @Override
    public void stayInPlace() {
        this.isMoving = false;
    }

    @Override
    public void goTo(Point point) {
        // TODO [NME] Must be implemented.
    }

    @Override
    public HitBox getHitBox() {
        return this.hitBox;
    }

    @Override
    public boolean isMoving() {
        return this.isMoving;
    }

    @Override
    public Wardrobe getWardrobe() {
        return this.wardrobe;
    }
    @Override
    public Body getBody() {
        return this.body;
    }

    @Override
    public Gender getGender() {
        return this.gender;
    }
    @Override
    public Currency getCurrency() {
        return this.currency;
    }
    @Override
    public String getName() {
        return this.name;
    }
    @Override
    public File getAvatarPicture() {
        return this.avatarPicture;
    }
    
}
