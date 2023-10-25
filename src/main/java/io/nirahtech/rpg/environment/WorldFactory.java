package io.nirahtech.rpg.environment;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.ResourceBundle;

import io.nirahtech.rpg.characters.Factory;

public final class WorldFactory implements Factory<World> {

    private static final String RESOURCE_FOLDER_OF_PLANETS = "world";

    private static World cachedWorld = null;

    private final ClassLoader getContextClassLoader() {
        return Thread.currentThread().getContextClassLoader();
    }

    private final InputStream getResourceAsStream(final String resource) {
        final InputStream in = this.getContextClassLoader().getResourceAsStream(resource);

        return in == null ? getClass().getResourceAsStream(resource) : in;
    }

    private final List<String> listResourceFiles(final String resourcesFolder) {
        List<String> filenames = new ArrayList<>();

        try (
                InputStream in = this.getResourceAsStream(resourcesFolder);
                BufferedReader br = new BufferedReader(new InputStreamReader(in))) {
            String resource;
            while ((resource = br.readLine()) != null) {
                filenames.add(resource);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return filenames;
    }

    private final City createCity(final String cityId, final ResourceBundle resourceBundle) {
        return new City(cityId, null, null, null, null);
    }

    private final Region createRegion(final String regionId, final ResourceBundle resourceBundle) {
        return new Region(null, 0, 0, null, null);
    }

    private final Continent createContinent(final String continentId, final ResourceBundle resourceBundle) {
        return new Continent(null, null);
    }

    private final Planet createPlanet(final String planetId, final ResourceBundle resourceBundle) {
        final String planetName = resourceBundle.getString("planet.name");
        return new Planet(planetName, null);
    }

    @Override
    public final synchronized World create() {
        World world = null;
        if (Objects.nonNull(WorldFactory.cachedWorld)) {
            world = WorldFactory.cachedWorld;
        } else {
            List<Planet> planets = new ArrayList<>();
            List<String> planetFiles = this.listResourceFiles(RESOURCE_FOLDER_OF_PLANETS);
            planetFiles = planetFiles.stream().filter(file -> file.startsWith("planet") && file.endsWith(".properties")).toList();
            planetFiles.forEach(file -> {
                final String fileNameWithoutExtension = file.split("\\.")[0];
                final ResourceBundle resourceBundle = ResourceBundle.getBundle(String.format("%s/%s", RESOURCE_FOLDER_OF_PLANETS, fileNameWithoutExtension));
                final String planetKey = resourceBundle.getString("planet.id");
                final Planet loadedPlanet = this.createPlanet(planetKey, resourceBundle);
                planets.add(loadedPlanet);
            });
            WorldFactory.cachedWorld = new World(null, planets);
            world = WorldFactory.cachedWorld;
        }
        return world;
    }
}
