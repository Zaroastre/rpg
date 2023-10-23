package io.nirahtech.rpg.strategies.attacks;

import java.util.Set;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.classes.ClassType;
import io.nirahtech.rpg.characters.classes.Guardian;
import io.nirahtech.rpg.characters.classes.Heal;
import io.nirahtech.rpg.characters.classes.SpellCurser;
import io.nirahtech.rpg.characters.classes.SpellDamager;
import io.nirahtech.rpg.characters.roles.Role;

public final class AttackStrategyChooser {

    private AttackStrategyChooser() { }

    private static final boolean isOnlyHealer(final Character<? extends CharacterClass> character) {
        final Set<Role> roles = character.getCharacterClass().getRoles();
        return !roles.isEmpty() && roles.contains(Role.HEAL);
    }
    private static final boolean isOnlyDamager(final Character<? extends CharacterClass> character) {
        final Set<Role> roles = character.getCharacterClass().getRoles();
        return !roles.isEmpty() && roles.contains(Role.DPS);
    }
    private static final boolean isOnlyProtector(final Character<? extends CharacterClass> character) {
        final Set<Role> roles = character.getCharacterClass().getRoles();
        return !roles.isEmpty() && roles.contains(Role.TANK);
    }



    public static final AttackStategy chooseBestStrategy(Character<? extends CharacterClass> attacker, Set<Character<? extends CharacterClass>> vilains) {
        
        AttackStategy attackStategy;
        // Examinez les caractéristiques de l'attaquant : le niveau, la classe, les armes, les compétences, etc..
        final ClassType classOfAttacker = attacker.getCharacterClass().getClassType();

        if (isOnlyHealer(attacker) && (classOfAttacker.getCharacterClass().isAssignableFrom(Heal.class) || classOfAttacker.getCharacterClass().isAssignableFrom(Guardian.class))) {

        }

        if (isOnlyDamager(attacker) && (classOfAttacker.getCharacterClass().isAssignableFrom(SpellDamager.class) || classOfAttacker.getCharacterClass().isAssignableFrom(SpellCurser.class))) {
            // Choisir le sort le plus adéquant, en fonction de la resource disponible de l'attanquant
        }

        if (isOnlyProtector(attacker) && classOfAttacker.getCharacterClass().isAssignableFrom(Heal.class)) {
            // Choisir le sort le plus adéquat en fonction des resources disponible de l'attaquant
        }

        /*
        Examinez les caractéristiques des cibles : Vous pouvez également examiner les caractéristiques des cibles, telles que leur niveau, leur rôle, leur vulnérabilité, etc.
        
        Évaluez le contexte : En fonction de ces caractéristiques, évaluez le contexte. Par exemple, si l'attaquant est un guerrier de haut niveau et que les cibles sont des ennemis faibles, vous pourriez choisir une stratégie d'attaque puissante. Si l'attaquant est vulnérable et les cibles sont fortes, vous pourriez choisir une stratégie de défense ou de fuite.
        
        Retournez la meilleure stratégie : Une fois que vous avez évalué le contexte, choisissez la stratégie d'attaque la plus appropriée parmi les stratégies disponibles et retournez-la.
         */
        attackStategy = new WeaponAttackStrategy(attacker.getWeapon());

        return attackStategy;
    }
}
