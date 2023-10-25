package io.nirahtech;

import io.nirahtech.rpg.environment.World;
import io.nirahtech.rpg.environment.WorldFactory;

/**
 * Unit test for simple App.
 */
public class AppTest 
{
    public static void main(String[] args) {
        final WorldFactory worldFactory = new WorldFactory();
        World world = worldFactory.create();
    }
}
