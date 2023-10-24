package io.nirahtech.rpg.interfaces.gui.components;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;

import io.nirahtech.rpg.environment.Planet;
import io.nirahtech.rpg.environment.World;

public final class RpgWindow {

    private final Dimension windowSize;
    private final JFrame frame;
    private final JPanel root;

    private final CreatorPanel creatorPanel;
    private InGamePanel inGamePanel;

    public RpgWindow() {
        this.windowSize = new Dimension(800, 600);
        this.root = new JPanel(new BorderLayout());
        this.frame = new JFrame("RPG");
        this.frame.add(this.root);
        this.creatorPanel = new CreatorPanel();
        this.root.add(this.creatorPanel);
        this.creatorPanel.addOnCharacterCreated((character) -> {
            System.out.println(String.format("%s was created!", character.getName()));

            final String worldName = UUID.randomUUID().toString();
            final Set<Planet> planets = new HashSet<>();
            planets.add(new Planet(UUID.randomUUID().toString(), null));
            planets.add(new Planet(UUID.randomUUID().toString(), null));
            final World world = new World(worldName, planets);
            world.planets().stream().findFirst().get().continents().stream().findFirst().get().regions().stream().findFirst().get();
            this.root.remove(this.creatorPanel);
            this.inGamePanel = new InGamePanel(character);
            this.root.add(this.inGamePanel);
            this.root.updateUI();
        });
    }

    public void display() {
        try {
            // On change le look and feel en cours
            UIManager.setLookAndFeel( "javax.swing.plaf.nimbus.NimbusLookAndFeel" );
            // On applique ce nouveau look à la fenêtre intégral 
            SwingUtilities.updateComponentTreeUI(this.frame);
        } catch( Exception exception ) { 
            exception.printStackTrace(); 
        }

        this.root.setBackground(Color.BLACK);
        
        this.frame.setPreferredSize(this.windowSize);
        this.frame.setSize(this.windowSize);
        this.frame.pack();
        this.frame.setVisible(true);
    }
}
