

public class SingleSourceAllDestinations {

    //public static final String fileName = "maze/100x100.txt";
    public static final String fileNamePrefix = "maze/";
    public static final String fileNamePostFix = ".txt";

    public static void main(String[] args) {

        GridGraph graph = GraphImporter.importGraphFromFile(fileNamePrefix+args[0]+fileNamePostFix);

        int sx = Integer.parseInt(args[1]);
        int sy = Integer.parseInt(args[2]);

        String delim = "";
        for (int y=0;y<graph.sizeY; ++y) {
            for (int x=0;x<graph.sizeX; ++x) {
                if (!graph.isBlocked(x,y)) {
                    float distance = test(graph, sx, sy, x, y);
                    System.out.print(delim);
                    System.out.print(x+"-"+y+"-"+distance);
                    delim = " ";
                }
            }
        }
    }

    public static float test(GridGraph graph, int sx, int sy, int ex, int ey) {
        // Use this for shortest 8-directional path
        //PathFindingAlgorithm algo = new JumpPointSearch(graph, sx, sy, ex, ey);
        
        // Use this for shortest Any-Angle path
        PathFindingAlgorithm algo = VisibilityGraphAlgorithm.graphReuse(graph, sx, sy, ex, ey);
        
        algo.computePath();
        return algo.getPathLength();
    }

}