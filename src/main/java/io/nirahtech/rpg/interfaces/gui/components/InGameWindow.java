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

import io.nirahtech.rpg.characters.Character;
import io.nirahtech.rpg.characters.classes.CharacterClass;
import io.nirahtech.rpg.environment.Planet;
import io.nirahtech.rpg.environment.World;

public final class InGameWindow {

    private final Dimension windowSize;
    private final JFrame frame;
    private final JPanel root;

    private final InGamePanel inGamePanel;
    
    public InGameWindow(World world, Character<? extends CharacterClass> character) {
        this.windowSize = new Dimension(800, 600);
        this.root = new JPanel(new BorderLayout());
        this.frame = new JFrame("RPG");
        this.frame.add(this.root);
        this.inGamePanel = new InGamePanel(world, character);
        this.root.add(this.inGamePanel);
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
        this.frame.setResizable(false);
        this.frame.setVisible(true);
    }
}
