package io.nirahtech.rpg.interfaces.gui.components;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridLayout;

import javax.swing.BoxLayout;
import javax.swing.JPanel;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.teams.Group;

public class InGamePanel extends JPanel {

    
    private final Character<? extends CharacterClass> character;
    private final Group group;

    private final GroupPanel groupPanel;
    
    public InGamePanel(Character<? extends CharacterClass> character) {
        super(new BorderLayout());
        this.character = character;
        this.group = Group.create(5);
        this.group.add(this.character);
        this.groupPanel = new GroupPanel(this.group);
        this.add(this.groupPanel, BorderLayout.WEST);
    }

    private final class GroupPanel extends JPanel {
        
        private final Group charactersGroup;

        private GroupPanel(final Group charactersGroup) {
            super(new GridLayout(charactersGroup.getMembers().size(), 1));
            this.charactersGroup = charactersGroup;
            this.setBackground(Color.RED);
            this.setPreferredSize(new Dimension(250, BoxLayout.Y_AXIS));;
        }
    }

    private final class CharacterMemberGroupPanel extends JPanel {

    }
}
