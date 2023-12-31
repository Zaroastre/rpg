package io.nirahtech.videogame;

import java.util.Optional;
import java.util.ResourceBundle;
import java.util.logging.Logger;

import io.nirahtech.rpg.interfaces.gui.components.GamePanel;
import io.nirahtech.videogame.artifacts.SuperObject;
import io.nirahtech.videogame.tile.Tile;
import io.nirahtech.videogame.tile.TileManager;

public class CollisionChecker implements Initializable {
    private static final Logger LOGGER = Logger.getLogger(CollisionChecker.class.getSimpleName());
    private static CollisionChecker instance;

    public static final CollisionChecker getInstance() {
        LOGGER.info("Calling unique instance of collision checker");
        if (CollisionChecker.instance == null) {
            CollisionChecker.instance = new CollisionChecker();
        }
        return CollisionChecker.instance;
    }

    private GamePanel gamePanel;

    private CollisionChecker() {

    }

    public void checkTile(final Character entity) {

        // Set rectangle perimeter for collision
        final int entityLeftWorldX = entity.getPositionOnTheWorldMap().x + entity.getSolidArea().x;
        final int entityRightWorldX = entity.getPositionOnTheWorldMap().x
                + (entity.getSolidArea().x + entity.getSolidArea().width);
        final int entityTopWorldY = entity.getPositionOnTheWorldMap().y + entity.getSolidArea().y;
        final int entityBottomWorldY = entity.getPositionOnTheWorldMap().y
                + (entity.getSolidArea().y + entity.getSolidArea().height);

        int entityLeftColumn = entityLeftWorldX / this.gamePanel.getTileSize();
        int entityRightColumn = entityRightWorldX / this.gamePanel.getTileSize();
        int entityTopRow = entityTopWorldY / this.gamePanel.getTileSize();
        int entityBottomRow = entityBottomWorldY / this.gamePanel.getTileSize();

        Tile tileNum1 = null, tileNum2 = null;
        // final WorldMap worldMap = TileManager.getInstance().getWorldMap();

        switch (entity.getDirection()) {
            case NORTH:
                // We are going to the top, we check 2 tiles in front of us.
                entityTopRow = (entityTopWorldY - entity.getSpeed()) / this.gamePanel.getTileSize();
                if (this.gamePanel.getPlayer().getPositionOnTheWorldMap().y > 0) {
                    // tileNum1 = worldMap.getTile(entityLeftColumn, entityTopRow);
                    // tileNum2 = worldMap.getTile(entityRightColumn, entityTopRow);
                } else {
                    entity.setCollision(true);
                }
                break;
            case EAST:
                entityRightColumn = (entityRightWorldX + entity.getSpeed()) / this.gamePanel.getTileSize();
                // if (this.gamePanel.getPlayer()
                //         .getPositionOnTheWorldMap().x < (worldMap
                //                 .getOriginalWidth() * this.gamePanel.getTileSize())) {
                //     tileNum1 = worldMap.getTile(entityRightColumn, entityTopRow);
                //     tileNum2 = worldMap.getTile(entityRightColumn,
                //             entityBottomRow);
                // } else {
                //     entity.setCollision(true);
                // }
                break;
            case SOUTH:
                // if (this.gamePanel.getPlayer()
                //         .getPositionOnTheWorldMap().y < (worldMap
                //                 .getOriginalHeight() * this.gamePanel.getTileSize())) {
                //     tileNum1 = worldMap.getTile(entityLeftColumn, entityBottomRow);
                //     tileNum2 = worldMap.getTile(entityRightColumn,
                //             entityBottomRow);
                // } else {
                //     entity.setCollision(true);
                // }
                break;
            case WEST:
                // entityLeftColumn = (entityRightWorldX - entity.getSpeed()) / this.gamePanel.getTileSize();
                // if (this.gamePanel.getPlayer().getPositionOnTheWorldMap().x > 0) {
                //     tileNum1 = worldMap.getTile(entityLeftColumn, entityTopRow);
                //     tileNum2 = worldMap.getTile(entityLeftColumn,
                //             entityBottomRow);
                // } else {
                //     entity.setCollision(true);
                // }
                break;
        }
        if (tileNum1 != null && tileNum2 != null) {
            entity.setCollision(tileNum1.isCollision() || tileNum2.isCollision());
        }
    }

    public Optional<Integer> checkSuperObject(final Character entity) {
        Optional<Integer> optionalIndex = Optional.empty();
        for (int i = 0; i < this.gamePanel.objects.length; i++) {
            SuperObject superObject = this.gamePanel.objects[i];
            if (superObject != null) {
                entity.getSolidArea().x = entity.getPositionOnTheWorldMap().x + entity.getSolidArea().x;
                entity.getSolidArea().y = entity.getPositionOnTheWorldMap().y + entity.getSolidArea().y;
                superObject.getSolidArea().x = superObject.getPositionOnTheWorldMap().x + superObject.getSolidArea().x;
                superObject.getSolidArea().y = superObject.getPositionOnTheWorldMap().y + superObject.getSolidArea().y;

                switch (entity.getDirection()) {
                    case NORTH:
                        entity.getSolidArea().y -= entity.getSpeed();
                        if (entity.getSolidArea().intersects(superObject.getSolidArea())) {
                            if (superObject.isCollision()) {
                                entity.setCollision(true);
                            }
                            if (entity instanceof Player) {
                                optionalIndex = Optional.of(i);
                            }
                        }
                        break;
                    case EAST:

                        entity.getSolidArea().x += entity.getSpeed();
                        if (entity.getSolidArea().intersects(superObject.getSolidArea())) {
                            if (superObject.isCollision()) {
                                entity.setCollision(true);
                            }
                            if (entity instanceof Player) {
                                optionalIndex = Optional.of(i);
                            }
                        }
                        break;
                    case SOUTH:

                        entity.getSolidArea().y += entity.getSpeed();
                        if (entity.getSolidArea().intersects(superObject.getSolidArea())) {
                            if (superObject.isCollision()) {
                                entity.setCollision(true);
                            }
                            if (entity instanceof Player) {
                                optionalIndex = Optional.of(i);
                            }
                        }
                        break;
                    case WEST:
                        entity.getSolidArea().x -= entity.getSpeed();
                        if (entity.getSolidArea().intersects(superObject.getSolidArea())) {
                            if (superObject.isCollision()) {
                                entity.setCollision(true);
                            }
                            if (entity instanceof Player) {
                                optionalIndex = Optional.of(i);
                            }
                        }
                        break;
                    default:
                        break;
                }
                entity.getSolidArea().x = entity.getSolidAreaDefaultLocation().x;
                entity.getSolidArea().y = entity.getSolidAreaDefaultLocation().y;
                superObject.getSolidArea().x = superObject.getSolidAreaDefaultLocation().x;
                superObject.getSolidArea().y = superObject.getSolidAreaDefaultLocation().y;
            }
        }
        return optionalIndex;
    }

    @Override
    public void initialize(ResourceBundle configuration) {
        LOGGER.info("Initializing collision checker instance...");
        this.gamePanel = GamePanel.getInstance();
        LOGGER.info("Collision checker instance initialized.");

    }
}
