
import java.awt.Color;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * ABSTRACT<br>
 * Template for all Path Finding Algorithms used.<br>
 */
public abstract class PathFindingAlgorithm {
    protected GridGraph graph;

    //protected int parent[];
    protected final int sizeX;
    protected final int sizeXplusOne;
    protected final int sizeY;

    protected final int sx;
    protected final int sy;
    protected final int ex;
    protected final int ey;
    
    private int ticketNumber = -1;
    
    private boolean recordingMode;
    private boolean usingStaticMemory = false;

    public PathFindingAlgorithm(GridGraph graph, int sizeX, int sizeY,
            int sx, int sy, int ex, int ey) {
        this.graph = graph;
        this.sizeX = sizeX;
        this.sizeXplusOne = sizeX+1;
        this.sizeY = sizeY;
        this.sx = sx;
        this.sy = sy;
        this.ex = ex;
        this.ey = ey;
    }
    
    protected void initialiseMemory(int size, float defaultDistance, int defaultParent, boolean defaultVisited) {
        usingStaticMemory = true;
        ticketNumber = Memory.initialise(size, defaultDistance, defaultParent, defaultVisited);
    }
    
    /**
     * Call this to compute the path.
     */
    public abstract void computePath();

    /**
     * @return retrieve the path computed by the algorithm
     */
    public abstract int[][] getPath();
    
    /**
     * @return directly get path length without computing path.
     * Has to run fast, unlike getPath.
     */
    protected abstract float getPathLength();
    
    protected int toOneDimIndex(int x, int y) {
        return graph.toOneDimIndex(x, y);
    }
    
    protected int toTwoDimX(int index) {
        return graph.toTwoDimX(index);
    }
    
    protected int toTwoDimY(int index) {
        return graph.toTwoDimY(index);
    }

    protected int goalParentIndex() {
        return toOneDimIndex(ex,ey);
    }
    
    /*protected int parent(int index) {
        return Memory.parent(index);
    }
    
    protected void setParent(int index, int value) {
        Memory.setParent(index, value);
    }
    
    protected int getSize() {
        return Memory.size();
    }*/
}
