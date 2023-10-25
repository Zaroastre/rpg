package io.nirahtech.rpg.interfaces.gui.components;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Objects;

import javax.imageio.ImageIO;
import javax.swing.BoxLayout;
import javax.swing.ImageIcon;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JProgressBar;

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
            this.setPreferredSize(new Dimension(250, BoxLayout.Y_AXIS));

            this.charactersGroup.getMembers().forEach(member -> {
                this.add(new CharacterMemberGroupPanel(member));
            });
        }
    }

    private final class CharacterMemberGroupPanel extends JPanel {
        private final Character<? extends CharacterClass> character;

        private final ImageIcon avatar;
        private final JLabel picture;
        private final JLabel username;
        private final JProgressBar life;
        private final JProgressBar resource;

        private CharacterMemberGroupPanel(final Character<? extends CharacterClass> character) {
            super(new BorderLayout());
            this.character = character;
            this.username = new JLabel(this.character.getName());
            this.life = new JProgressBar(0, this.character.getLife().getMaximumPoints());
            this.life.setValue(this.character.getLife().getPoints());
            this.resource = new JProgressBar(0, this.character.getCharacterClass().getResource().getMaximumPoints());
            this.resource.setValue(this.character.getCharacterClass().getResource().getPoints());
            Dimension picsize = new Dimension(100, 100);
            if (Objects.nonNull(this.character.getAvatarPicture())) {
                this.avatar = new ImageIcon(this.character.getAvatarPicture().getAbsolutePath());
                this.picture = new JLabel(this.avatar);
            } else {
                BufferedImage img = null;
                try {
                    img = ImageIO.read(new File("head.png"));
                    Image dimg = img.getScaledInstance((int)picsize.getWidth(), (int)picsize.getHeight(),
                            Image.SCALE_SMOOTH);

                            this.avatar = new ImageIcon(dimg);
                            this.picture = new JLabel(this.avatar);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            final JPanel container = new JPanel(new GridLayout(3, 1));
            this.picture.setPreferredSize(picsize);
            this.picture.setBackground(Color.RED);
            container.add(this.username);
            container.add(this.life);
            container.add(this.resource);
            this.add(this.picture, BorderLayout.WEST);
            this.add(container, BorderLayout.CENTER);
            this.setPreferredSize(new Dimension(100, 50));
        }
    }
}
