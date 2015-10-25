import java.util.ArrayList;
import java.util.Iterator;

//import algorithms.priorityqueue.IndirectHeap;

public class VisibilityGraphAlgorithm extends PathFindingAlgorithm {
    protected VisibilityGraph visibilityGraph;
    protected boolean reuseGraph = false;
    protected boolean slowDijkstra = false;

    protected Float[] distance;
    protected boolean[] visited;
    
    protected ReusableIndirectHeap pq;

    protected int finish;
    
    public VisibilityGraphAlgorithm(GridGraph graph, int sx, int sy, int ex, int ey) {
        super(graph, graph.sizeX, graph.sizeY, sx, sy, ex, ey);
    }

    public static VisibilityGraphAlgorithm graphReuse(GridGraph graph, int sx, int sy, int ex, int ey) {
        VisibilityGraphAlgorithm algo = new VisibilityGraphAlgorithm(graph, sx, sy, ex, ey);
        algo.reuseGraph = true;
        return algo;
    }
    
    public VisibilityGraph getVisibilityGraph() {
        return visibilityGraph;
    }
    
    @Override
    public void computePath() {
        setupVisibilityGraph();

        int totalSize = visibilityGraph.size();
        pq = new ReusableIndirectHeap(totalSize);
        this.initialiseMemory(totalSize, Float.POSITIVE_INFINITY, -1, false);
        
        initialise(visibilityGraph.startNode());

        /*distance = new Float[visibilityGraph.size()];
        parent = new int[visibilityGraph.size()];
        initialise(visibilityGraph.startNode());
        visited = new boolean[visibilityGraph.size()];*/
        
        int finish = visibilityGraph.endNode();
        while (!pq.isEmpty()) {
            int current = pq.popMinIndex();
            setVisited(current, true);
            
            if (current == finish) {
                break;
            }
            
            Iterator<Edge> itr = visibilityGraph.edgeIterator(current);
            while (itr.hasNext()) {
                Edge edge = itr.next();
                if (!visited(edge.dest) && relax(edge)) {
                    // If relaxation is done.
                    Point dest = visibilityGraph.coordinateOf(edge.dest);
                    pq.decreaseKey(edge.dest, distance(edge.dest) + heuristic(dest.x, dest.y));
                }
            }
        }
    }

    protected final void initialise(int s) {
        pq.decreaseKey(s, 0f);
        Memory.setDistance(s, 0f);
    }

    protected void setupVisibilityGraph() {
        if (reuseGraph) {
            visibilityGraph = VisibilityGraph.getStoredGraph(graph, sx, sy, ex, ey);
        } else {
            visibilityGraph = new VisibilityGraph(graph, sx, sy, ex, ey);
        }
        
        visibilityGraph.initialise();
    }

    protected float heuristic(int x, int y) {
        return graph.distance(x, y, ex, ey);
    }

    
    protected final boolean relax(Edge edge) {
        // return true iff relaxation is done.
        return relax(edge.source, edge.dest, edge.weight);
    }

    protected final boolean relax(int u, int v, float weightUV) {
        // return true iff relaxation is done.
        float newWeight = distance(u) + weightUV;
        if (newWeight < distance(v)) {
            setDistance(v, newWeight);
            setParent(v, u);
            return true;
        }
        return false;
    }
    

    private int pathLength() {
        int length = 0;
        int current = visibilityGraph.endNode();
        while (current != -1) {
            current = parent(current);
            length++;
        }
        return length;
    }

    @Override
    public int[][] getPath() {
        int length = pathLength();
        int[][] path = new int[length][];
        int current = visibilityGraph.endNode();
        
        int index = length-1;
        while (current != -1) {
            Point point = visibilityGraph.coordinateOf(current);
            int x = point.x;
            int y = point.y;
            
            path[index] = new int[2];
            path[index][0] = x;
            path[index][1] = y;
            
            index--;
            current = parent(current);
        }
        
        return path;
    }

    @Override
    protected float getPathLength() {
        int[][] path = getPath();
        float pathLength = 0;
        for (int i=0; i<path.length-1; i++) {
            pathLength += graph.distance(path[i][0], path[i][1],
                            path[i+1][0], path[i+1][1]);
        }
        return pathLength;
    }
    
    /** REGION - EVEN MORE USELESS */
    protected int parent(int index) {
        return Memory.parent(index);
    }
    
    protected void setParent(int index, int value) {
        Memory.setParent(index, value);
    }
    
    protected float distance(int index) {
        return Memory.distance(index);
    }
    
    protected void setDistance(int index, float value) {
        Memory.setDistance(index, value);
    }
    
    protected boolean visited(int index) {
        return Memory.visited(index);
    }
    
    protected void setVisited(int index, boolean value) {
        Memory.setVisited(index, value);
    }
}
