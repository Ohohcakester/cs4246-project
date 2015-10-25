import java.util.Arrays;

public class Compute {

    //public static final String fileName = "maze/100x100.txt";
    public static final String fileNamePrefix = "maze/";
    public static final String fileNamePostFix = ".txt";

    public static void main(String[] args) {
        //testSpeed();
        GridGraph graph = GraphImporter.importGraphFromFile(fileNamePrefix+args[0]+fileNamePostFix);
        
        String delim = "";
        for (String query : args) {
            if (query == args[0]) continue;
            System.out.print(delim);
            System.out.print(parseTest(graph, query));
            delim = " ";
        }
    }
    
    public static float parseTest(GridGraph graph, String query) {
        String[] params = query.split("-");
        return test(graph,Integer.parseInt(params[0]),Integer.parseInt(params[1]),Integer.parseInt(params[2]),Integer.parseInt(params[3]));
    }

    public static float test(GridGraph graph, int sx, int sy, int ex, int ey) {
        // Use this for shortest 8-directional path
        //PathFindingAlgorithm algo = new JumpPointSearch(graph, sx, sy, ex, ey);
        
        // Use this for shortest Any-Angle path
        PathFindingAlgorithm algo = VisibilityGraphAlgorithm.graphReuse(graph, sx, sy, ex, ey);
        
        algo.computePath();
        return algo.getPathLength();

        //int[][] path = algo.getPath();
        //System.out.println(Arrays.deepToString(path));
        //System.out.println("Length: " + length);
    }


    public static void printGraph(GridGraph graph) {
        for (int j=0;j<graph.sizeY;++j) {
            for (int i=0;i<graph.sizeX;++i) {
                System.out.print(graph.isBlocked(i,j)?1:0);
            }
            System.out.println();
        }
    }

    public static void testPrint(GridGraph graph, int sx, int sy, int ex, int ey) {
        System.out.println(test(graph,sx,sy,ex,ey));
    }


    public static void testSpeed() {
        String fileName = "maze/100x100.txt";
        GridGraph graph = GraphImporter.importGraphFromFile(fileName);
        System.out.println("Start");
        for (int i=0;i<1;++i) {
            testPrint(graph, 1,42,75,81);
            testPrint(graph, 100,0,99,2);
            testPrint(graph, 11,56,56,16);
            testPrint(graph, 11,99,94,35);
            testPrint(graph, 18,29,92,91);
            testPrint(graph, 18,37,57,18);
            testPrint(graph, 19,94,23,14);
            testPrint(graph, 20,17,58,44);
            testPrint(graph, 22,44,47,31);
            testPrint(graph, 27,27,20,23);
            testPrint(graph, 3,77,30,37);
            testPrint(graph, 32,10,1,63);
            testPrint(graph, 33,24,34,57);
            testPrint(graph, 40,57,31,28);
            testPrint(graph, 42,26,7,62);
            testPrint(graph, 43,26,81,90);
            testPrint(graph, 44,8,49,28);
            testPrint(graph, 45,49,46,4);
            testPrint(graph, 5,51,48,56);
            testPrint(graph, 5,70,36,96);
            testPrint(graph, 51,33,37,44);
            testPrint(graph, 51,89,44,97);
            testPrint(graph, 52,9,32,95);
            testPrint(graph, 53,28,90,10);
            testPrint(graph, 60,20,69,18);
            testPrint(graph, 61,52,46,3);
            testPrint(graph, 61,98,46,66);
            testPrint(graph, 63,49,17,63);
            testPrint(graph, 65,52,66,74);
            testPrint(graph, 67,77,57,25);
            testPrint(graph, 7,24,67,63);
            testPrint(graph, 70,71,51,69);
            testPrint(graph, 70,99,50,43);
            testPrint(graph, 72,79,94,83);
            testPrint(graph, 75,25,65,91);
            testPrint(graph, 76,76,67,32);
            testPrint(graph, 78,10,74,96);
            testPrint(graph, 79,19,64,23);
            testPrint(graph, 8,42,36,60);
            testPrint(graph, 82,95,98,25);
            testPrint(graph, 86,18,29,66);
            testPrint(graph, 86,70,11,20);
            testPrint(graph, 86,80,78,53);
            testPrint(graph, 88,19,77,15);
            testPrint(graph, 9,26,43,15);
            testPrint(graph, 9,92,13,59);
            testPrint(graph, 90,49,39,64);
            testPrint(graph, 91,66,58,75);
            testPrint(graph, 91,97,60,94);
            testPrint(graph, 98,27,33,49);
        }
        System.out.println("Finish");
    }
}