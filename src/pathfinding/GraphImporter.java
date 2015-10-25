
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

/**
 * How to create a grid file.<br>
 * The grid is stored in a .txt file in the following format:<br>
 * <pre>
 * 6 3
 * 0 1 0 0 1 0
 * 0 1 1 1 1 0
 * 0 1 0 0 1 0</pre>
 * 
 * The first number specifies the number of columns of the grid.<br>
 * The second number specifies the number of rows of the grid.<br>
 * The rest of the numbers specify the status of the tiles. 1 means a blocked
 * tile, 0 means an unblocked tile.
 */
public class GraphImporter {
    private GridGraph gridGraph;
    
    private GraphImporter(String fileName) {
        boolean[][] result = null;

        File file = new File(fileName);
        try {
            FileReader fileReader = new FileReader(file);
            Scanner sc = new Scanner(fileReader);
            int x = sc.nextInt();
            int y = sc.nextInt();
            result = new boolean[y][];
            for (int i=0; i<y; i++) {
                result[i] = new boolean[x];
                for (int j=0; j<x; j++) {
                    result[i][j] = (sc.nextInt() != 0);
                }
            }
            sc.close();
        } catch (FileNotFoundException e) {
            System.out.println("File " + fileName + " not found!");
        }
        
        create(result);          
    }

    private void create(boolean[][] result) {
        gridGraph = new GridGraph(result[0].length, result.length);
        for (int y=0;y<result.length;y++) {
            for (int x=0;x<result[0].length;x++) {
                gridGraph.setBlocked(x, y, result[y][x]);
            }
        }
    }

    private void createDoubleSize(boolean[][] result) {
        int size = 2;
        
        gridGraph = new GridGraph(result[0].length*size, result.length*size);
        for (int y=0;y<result.length*size;y++) {
            for (int x=0;x<result[0].length*size;x++) {
                gridGraph.setBlocked(x, y, result[y/size][x/size]);
            }
        }
    }
    
    private GridGraph retrieve() {
        return gridGraph;
    }
    
    /**
     * Import a graph from a file in the AnyAnglePathFinding directory.
     * Look into the GraphImporter documentation for details on how to create a grid file.
     */
    public static GridGraph importGraphFromFile(String filename) {
        GridGraph gridGraph;
        GraphImporter graphImporter = new GraphImporter(filename);
        gridGraph = graphImporter.retrieve();
        return gridGraph;
    }
    
    private static HashMap<String, String> readFile(File file) {
        HashMap<String,String> dict = new HashMap<>();
        try {
            FileReader fr = new FileReader(file);
            BufferedReader br = new BufferedReader(fr);
            String s = br.readLine();
            while (s != null) {
                put(dict, s);
                s = br.readLine();
            }
    
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        return dict;
    }
        
    private static void put(HashMap<String,String> dict, String input) {
        String[] args = input.split(":", 2);
        dict.put(args[0].trim(), args[1].trim());
    }

}
