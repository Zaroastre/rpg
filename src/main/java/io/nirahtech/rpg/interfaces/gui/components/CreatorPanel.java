package io.nirahtech.rpg.interfaces.gui.components;

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.util.Objects;
import java.util.function.Consumer;

import javax.swing.DefaultComboBoxModel;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.JTextField;

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.CharacterFactory;
import io.nirahtech.rpg.characters.Faction;
import io.nirahtech.rpg.characters.Gender;
import io.nirahtech.rpg.characters.Level;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.characters.classes.ClassType;
import io.nirahtech.rpg.characters.races.BreedType;

public class CreatorPanel extends JPanel {

    private final JPanel usernamePanel;
    private final JLabel usernameLabel;
    private final JTextField usernameTextField;

    private final JPanel genderPanel;
    private final JLabel genderLabel;
    private final JComboBox<Gender> genderComboBox;

    private final JPanel classPanel;
    private final JLabel classLabel;
    private final JComboBox<ClassType> classComboBox;

    private final JPanel breedPanel;
    private final JLabel breedLabel;
    private final JComboBox<BreedType> breedComboBox;

    private final JPanel factionPanel;
    private final JLabel factionLabel;
    private final JComboBox<Faction> factionComboBox;

    private final JPanel levelPanel;
    private final JLabel levelLabel;
    private final JSlider levelSlider;

    private final JPanel actionPanel;
    private final JLabel actionLabel;
    private final JButton creatorButton;

    private Consumer<Character<? extends CharacterClass>> onClickCallback = null;

    public void addOnCharacterCreated(final Consumer<Character<? extends CharacterClass>> callback) {
        this.onClickCallback = callback;
    }

    public CreatorPanel() {
        super(new GridLayout(7, 1));
        this.usernamePanel = new JPanel(new GridLayout(1, 2));
        this.usernameLabel = new JLabel("Username");
        this.usernameTextField = new JTextField();
        this.usernamePanel.add(this.usernameLabel);
        this.usernamePanel.add(this.usernameTextField);

        this.genderPanel = new JPanel(new GridLayout(1, 2));
        this.genderLabel = new JLabel("Gender");
        this.genderComboBox = new JComboBox<>(new GenderComboBoxModel(Gender.values()));
        this.genderPanel.add(this.genderLabel);
        this.genderPanel.add(this.genderComboBox, BorderLayout.CENTER);

        this.breedPanel = new JPanel(new GridLayout(1, 2));
        this.breedLabel = new JLabel("Breed");
        this.breedComboBox = new JComboBox<>(new BreedComboBoxModel(BreedType.values()));
        this.breedPanel.add(this.breedLabel);
        this.breedPanel.add(this.breedComboBox);

        this.classPanel = new JPanel(new GridLayout(1, 2));
        this.classLabel = new JLabel("Class");
        this.classComboBox = new JComboBox<>(ClassType.values());
        this.classPanel.add(this.classLabel);
        this.classPanel.add(this.classComboBox);

        this.factionPanel = new JPanel(new GridLayout(1, 2));
        this.factionLabel = new JLabel("Faction");
        this.factionComboBox = new JComboBox<>(Faction.values());
        this.factionPanel.add(this.factionLabel);
        this.factionPanel.add(this.factionComboBox);

        this.levelPanel = new JPanel(new GridLayout(1, 2));
        this.levelLabel = new JLabel("Level");
        this.levelSlider = new JSlider(1, 40, 1);
        this.levelSlider.setPaintTrack(true);
        this.levelSlider.setPaintTicks(true);
        this.levelSlider.setPaintLabels(true);
        this.levelPanel.add(this.levelLabel);
        this.levelPanel.add(this.levelSlider);

        this.actionPanel = new JPanel(new GridLayout(1, 2));
        this.actionLabel = new JLabel("Actions");
        this.creatorButton = new JButton("Create");
        this.actionPanel.add(this.actionLabel);
        this.actionPanel.add(this.creatorButton);
        this.creatorButton.addActionListener((event) -> {
            final String name = this.usernameTextField.getText();
            final BreedType breedType = (BreedType) this.breedComboBox.getSelectedItem();
            final ClassType characterClassType = (ClassType) this.classComboBox.getSelectedItem();
            final Gender gender = (Gender) this.genderComboBox.getSelectedItem();
            final Level level = Level.Factory.create(this.levelSlider.getValue());
            final Faction faction = (Faction) this.factionComboBox.getSelectedItem();
            final Character<? extends CharacterClass> character = CharacterFactory.create(
                        name, 
                        breedType.create(),
                        characterClassType.create(),
                        gender,
                        faction,
                        level);
            if (Objects.nonNull(this.onClickCallback)) {
                this.onClickCallback.accept(character);
            }
        });

        this.add(this.usernamePanel);
        this.add(this.genderPanel);
        this.add(this.breedPanel);
        this.add(this.classPanel);
        this.add(this.factionPanel);
        this.add(this.levelPanel);
        this.add(this.actionPanel);
    }

    private final class GenderComboBoxModel extends DefaultComboBoxModel<Gender> {
        public GenderComboBoxModel(Gender[] items) {
            super(items);
        }

        @Override
        public Gender getSelectedItem() {
            final Gender item = (Gender) super.getSelectedItem();
            return item;
        }
    }

    private final class BreedComboBoxModel extends DefaultComboBoxModel<BreedType> {
        public BreedComboBoxModel(BreedType[] items) {
            super(items);
        }

        @Override
        public BreedType getSelectedItem() {
            final BreedType item = (BreedType) super.getSelectedItem();
            return item;
        }
    }
}
