import java.util.Arrays;

public class Compute {

    public static final String fileName = "maze/100x100.txt";

    public static void main(String[] args) {
        GridGraph graph = GraphImporter.importGraphFromFile(fileName);
        //search(graph);
    }

    public static void test(GridGraph graph, int sx, int sy, int ex, int ey) {
        JumpPointSearch jps = new JumpPointSearch(graph, sx, sy, ex, ey);
        jps.computePath();
        int[][] path = jps.getPath();
        float length = jps.getPathLength();
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


    public static void testSpeed() {
        System.out.println("Start");
        for (int i=0;i<1000;++i) {
            test(graph, 1,42,75,81);
            test(graph, 100,0,99,2);
            test(graph, 11,56,56,16);
            test(graph, 11,99,94,35);
            test(graph, 18,29,92,91);
            test(graph, 18,37,57,18);
            test(graph, 19,94,23,14);
            test(graph, 20,17,58,44);
            test(graph, 22,44,47,31);
            test(graph, 27,27,20,23);
            test(graph, 3,77,30,37);
            test(graph, 32,10,1,63);
            test(graph, 33,24,34,57);
            test(graph, 40,57,31,28);
            test(graph, 42,26,7,62);
            test(graph, 43,26,81,90);
            test(graph, 44,8,49,28);
            test(graph, 45,49,46,4);
            test(graph, 5,51,48,56);
            test(graph, 5,70,36,96);
            test(graph, 51,33,37,44);
            test(graph, 51,89,44,97);
            test(graph, 52,9,32,95);
            test(graph, 53,28,90,10);
            test(graph, 60,20,69,18);
            test(graph, 61,52,46,3);
            test(graph, 61,98,46,66);
            test(graph, 63,49,17,63);
            test(graph, 65,52,66,74);
            test(graph, 67,77,57,25);
            test(graph, 7,24,67,63);
            test(graph, 70,71,51,69);
            test(graph, 70,99,50,43);
            test(graph, 72,79,94,83);
            test(graph, 75,25,65,91);
            test(graph, 76,76,67,32);
            test(graph, 78,10,74,96);
            test(graph, 79,19,64,23);
            test(graph, 8,42,36,60);
            test(graph, 82,95,98,25);
            test(graph, 86,18,29,66);
            test(graph, 86,70,11,20);
            test(graph, 86,80,78,53);
            test(graph, 88,19,77,15);
            test(graph, 9,26,43,15);
            test(graph, 9,92,13,59);
            test(graph, 90,49,39,64);
            test(graph, 91,66,58,75);
            test(graph, 91,97,60,94);
            test(graph, 98,27,33,49);
        }
        System.out.println("Finish");
    }
}