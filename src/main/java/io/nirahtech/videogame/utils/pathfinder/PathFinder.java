package io.nirahtech.videogame.utils.pathfinder;

import java.util.List;
import java.awt.Point;

public interface PathFinder {
    List<Node> search(Point a, Point b);

    List<Node> search();

    void setStartNode(final int column, final int row);

    void setGoalNode(final int column, final int row);

    void setSolidNode(final int column, final int row);
}
