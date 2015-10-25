
public class JumpPointSearch extends PathFindingAlgorithm {
    protected boolean postSmoothingOn = false;

    protected ReusableIndirectHeap pq; 

    protected int finish;

    protected int[] neighboursdX;
    protected int[] neighboursdY;
    protected int neighbourCount;

    public JumpPointSearch(GridGraph graph, int sx, int sy, int ex, int ey) {
        super(graph, graph.sizeX, graph.sizeY, sx, sy, ex, ey);
    }
    
    public static JumpPointSearch postSmooth(GridGraph graph, int sx, int sy, int ex, int ey) {
        JumpPointSearch algo = new JumpPointSearch(graph, sx, sy, ex, ey);
        algo.postSmoothingOn = true;
        return algo;
    }

    protected final void initialise(int s) {
        pq.decreaseKey(s, 0f);
        Memory.setDistance(s, 0f);
    }

    @Override
    public void computePath() {
        neighboursdX = new int[8];
        neighboursdY = new int[8];
        neighbourCount = 0;
        
        int totalSize = (graph.sizeX+1) * (graph.sizeY+1);

        int start = toOneDimIndex(sx, sy);
        finish = toOneDimIndex(ex, ey);
        
        pq = new ReusableIndirectHeap(totalSize);
        this.initialiseMemory(totalSize, Float.POSITIVE_INFINITY, -1, false);
        
        initialise(start);
        
        while (!pq.isEmpty()) {
            int current = pq.popMinIndex();
            if (current == finish || distance(current) == Float.POSITIVE_INFINITY) {
                break;
            }

            setVisited(current, true);

            int x = toTwoDimX(current);
            int y = toTwoDimY(current);
            
            computeNeighbours(current, x, y); // stores neighbours in attribute.

            for (int i=0;i<neighbourCount;++i) {
                int dx = neighboursdX[i];
                int dy = neighboursdY[i];
                
                int successor = jump(x, y, dx, dy);
                if (successor != -1) {
                    tryRelax(current, x, y, successor);
                }
            }
        }

        maybePostSmooth();
    }
    
    protected int jump(int x, int y, int dx, int dy) {
        if (dx < 0) {
            if (dy < 0) {
                return jumpDL(x,y);
            } else if (dy > 0) {
                return jumpUL(x,y);
            } else {
                return jumpL(x,y);
            }
        } else if (dx > 0) {
            if (dy < 0) {
                return jumpDR(x,y);
            } else if (dy > 0) {
                return jumpUR(x,y);
            } else {
                return jumpR(x,y);
            }
        } else {
            if (dy < 0) {
                return jumpD(x,y);
            } else {
                return jumpU(x,y);
            }
        }
        
    }
    
    private int jumpDL(int x, int y) {
        while(true) {
            x -= 1;
            y -= 1;
            if (graph.isBlocked(x, y)) return -1;
            if (x == ex && y == ey) return toOneDimIndex(x,y);
            // diagonal cannot be forced on vertices.
            if (jumpL(x,y) != -1) return toOneDimIndex(x,y);
            if (jumpD(x,y) != -1) return toOneDimIndex(x,y);
        }
    }
    
    private int jumpDR(int x, int y) {
        while(true) {
            x += 1;
            y -= 1;
            if (graph.isBlocked(x-1, y)) return -1;
            if (x == ex && y == ey) return toOneDimIndex(x,y);
            // diagonal cannot be forced on vertices.
            if (jumpD(x,y) != -1) return toOneDimIndex(x,y);
            if (jumpR(x,y) != -1) return toOneDimIndex(x,y);
        }
    }
    
    private int jumpUL(int x, int y) {
        while(true) {
            x -= 1;
            y += 1;
            if (graph.isBlocked(x, y-1)) return -1;
            if (x == ex && y == ey) return toOneDimIndex(x,y);
            // diagonal cannot be forced on vertices.
            if (jumpL(x,y) != -1) return toOneDimIndex(x,y);
            if (jumpU(x,y) != -1) return toOneDimIndex(x,y);
        }
    }
    
    private int jumpUR(int x, int y) {
        while(true) {
            x += 1;
            y += 1;
            if (graph.isBlocked(x-1, y-1)) return -1;
            if (x == ex && y == ey) return toOneDimIndex(x,y);
            // diagonal cannot be forced on vertices.
            if (jumpU(x,y) != -1) return toOneDimIndex(x,y);
            if (jumpR(x,y) != -1) return toOneDimIndex(x,y);
        }
    }
    
    private int jumpL(int x, int y) {
        while(true) {
            x -= 1;
            if (graph.isBlocked(x, y)) {
                if (graph.isBlocked(x, y-1)) {
                    return -1;
                } else {
                    if (!graph.isBlocked(x-1, y)) return toOneDimIndex(x,y);
                }
            }
            if (graph.isBlocked(x, y-1)) {
                if (!graph.isBlocked(x-1, y-1)) return toOneDimIndex(x,y);
            }
            if (x == ex && y == ey) return toOneDimIndex(x,y);
        }
    }
    
    private int jumpR(int x, int y) {
        while(true) {
            x += 1;
            if (graph.isBlocked(x-1, y)) {
                if (graph.isBlocked(x-1, y-1)) {
                    return -1;
                } else {
                    if (!graph.isBlocked(x, y)) return toOneDimIndex(x,y);
                }
            }
            if (graph.isBlocked(x-1, y-1)) {
                if (!graph.isBlocked(x, y-1)) return toOneDimIndex(x,y);
            }
            if (x == ex && y == ey) return toOneDimIndex(x,y);
        }
    }
    
    private int jumpD(int x, int y) {
        while(true) {
            y -= 1;
            if (graph.isBlocked(x, y)) {
                if (graph.isBlocked(x-1, y)) {
                    return -1;
                } else {
                    if (!graph.isBlocked(x, y-1)) return toOneDimIndex(x,y);
                }
            }
            if (graph.isBlocked(x-1, y)) {
                if (!graph.isBlocked(x-1, y-1)) return toOneDimIndex(x,y);
            }
            if (x == ex && y == ey) return toOneDimIndex(x,y);
        }
    }
    
    private int jumpU(int x, int y) {
        while(true) {
            y += 1;
            if (graph.isBlocked(x, y-1)) {
                if (graph.isBlocked(x-1, y-1)) {
                    return -1;
                } else {
                    if (!graph.isBlocked(x, y)) return toOneDimIndex(x,y);
                }
            }
            if (graph.isBlocked(x-1, y-1)) {
                if (!graph.isBlocked(x-1, y)) return toOneDimIndex(x,y);
            }
            if (x == ex && y == ey) return toOneDimIndex(x,y);
        }
    }

    protected void computeNeighbours(int currentIndex, int cx, int cy) {
        neighbourCount = 0;

        int parentIndex = parent(currentIndex);
        if (parentIndex == -1) {
            // is start node.
            for (int y=-1;y<=1;++y) {
                for (int x=-1;x<=1;++x) {
                    if (x == 0 && y == 0) continue;
                    int px = cx+x;
                    int py = cy+y;
                    if (graph.neighbourLineOfSight(cx,cy,px,py)) {
                        addNeighbour(x, y);
                    }
                }
            }
            return;
        }
        
        int dirX = cx - this.toTwoDimX(parentIndex);
        int dirY = cy - this.toTwoDimY(parentIndex);

        if (dirX < 0) {
            if (dirY < 0) {
                // down-left
                if (!graph.isBlocked(cx-1, cy-1)) {
                    addNeighbour(-1,-1);
                    addNeighbour(-1,0);
                    addNeighbour(0,-1);
                } else {
                    if (!graph.isBlocked(cx-1, cy)) addNeighbour(-1,0);
                    if (!graph.isBlocked(cx, cy-1)) addNeighbour(0,-1);
                }
            } else if (dirY > 0) {
                // up-left
                if (!graph.isBlocked(cx-1, cy)) {
                    addNeighbour(-1,1);
                    addNeighbour(-1,0);
                    addNeighbour(0,1);
                } else {
                    if (!graph.isBlocked(cx-1, cy-1)) addNeighbour(-1,0);
                    if (!graph.isBlocked(cx, cy)) addNeighbour(0,1);
                }
            } else {
                // left
                if (graph.isBlocked(cx,cy)) {
                    if (!graph.isBlocked(cx-1, cy)) {
                        addNeighbour(-1,1);
                        addNeighbour(0,1);
                        addNeighbour(-1,0);
                    } else {
                        throw new UnsupportedOperationException("wrong");
                    }
                } else if (graph.isBlocked(cx,cy-1)) {
                    if (!graph.isBlocked(cx-1, cy-1)) {
                        addNeighbour(-1,-1);
                        addNeighbour(0,-1);
                        addNeighbour(-1,0);
                    } else {
                        throw new UnsupportedOperationException("wrong");
                    }
                } else {
                    throw new UnsupportedOperationException("wrong");
                }
            }
        } else if (dirX > 0) {
            if (dirY < 0) {
                // down-right
                if (!graph.isBlocked(cx, cy-1)) {
                    addNeighbour(1,-1);
                    addNeighbour(1,0);
                    addNeighbour(0,-1);
                } else {
                    if (!graph.isBlocked(cx, cy)) addNeighbour(1,0);
                    if (!graph.isBlocked(cx-1, cy-1)) addNeighbour(0,-1);
                }
            } else if (dirY > 0) {
                // up-right
                if (!graph.isBlocked(cx, cy)) {
                    addNeighbour(1,1);
                    addNeighbour(1,0);
                    addNeighbour(0,1);
                } else {
                    if (!graph.isBlocked(cx, cy-1)) addNeighbour(1,0);
                    if (!graph.isBlocked(cx-1, cy)) addNeighbour(0,1);
                }
            } else {
                // right
                if (graph.isBlocked(cx-1,cy)) {
                    if (!graph.isBlocked(cx, cy)) {
                        addNeighbour(1,1);
                        addNeighbour(0,1);
                        addNeighbour(1,0);
                    } else {
                        throw new UnsupportedOperationException("wrong");
                    }
                } else if (graph.isBlocked(cx-1,cy-1)) {
                    if (!graph.isBlocked(cx, cy-1)) {
                        addNeighbour(1,-1);
                        addNeighbour(0,-1);
                        addNeighbour(1,0);
                    } else {
                        throw new UnsupportedOperationException("wrong");
                    }
                } else {
                    throw new UnsupportedOperationException("wrong");
                }
            }
        } else {
            if (dirY < 0) {
                // down
                if (graph.isBlocked(cx,cy)) {
                    if (!graph.isBlocked(cx, cy-1)) {
                        addNeighbour(1,-1);
                        addNeighbour(1,0);
                        addNeighbour(0,-1);
                    } else {
                        throw new UnsupportedOperationException("wrong");
                    }
                } else if (graph.isBlocked(cx-1,cy)) {
                    if (!graph.isBlocked(cx-1, cy-1)) {
                        addNeighbour(-1,-1);
                        addNeighbour(-1,0);
                        addNeighbour(0,-1);
                    } else {
                        throw new UnsupportedOperationException("wrong");
                    }
                } else {
                    throw new UnsupportedOperationException("wrong");
                }
            } else { //dirY > 0
                // up
                if (graph.isBlocked(cx,cy-1)) {
                    if (!graph.isBlocked(cx, cy)) {
                        addNeighbour(1,1);
                        addNeighbour(1,0);
                        addNeighbour(0,1);
                    } else {
                        throw new UnsupportedOperationException("wrong");
                    }
                } else if (graph.isBlocked(cx-1,cy-1)) {
                    if (!graph.isBlocked(cx-1, cy)) {
                        addNeighbour(-1,1);
                        addNeighbour(-1,0);
                        addNeighbour(0,1);
                    } else {
                        throw new UnsupportedOperationException("wrong");
                    }
                } else {
                    throw new UnsupportedOperationException("wrong");
                }
            }
        }
    }
    
    private void addNeighbour(int x, int y) {
        neighboursdX[neighbourCount] = x;
        neighboursdY[neighbourCount] = y;
        neighbourCount++;
    }

    protected float heuristic(int x, int y) {
        return graph.octileDistance(x, y, ex, ey);
    }

    protected void tryRelax(int current, int currX, int currY, int destination) {
        if (visited(destination)) return;

        int destX = toTwoDimX(destination);
        int destY = toTwoDimY(destination);
        
        if (relax(current, destination, graph.octileDistance(currX, currY, destX, destY))) {
            // If relaxation is done.
            pq.decreaseKey(destination, distance(destination) + heuristic(destX,destY));
        }
    }

    protected boolean relax(int u, int v, float weightUV) {
        // return true iff relaxation is done.
        
        float newWeight = distance(u) + weightUV;
        if (newWeight < distance(v)) {
            setDistance(v, newWeight);
            setParent(v, u);
            //maybeSaveSearchSnapshot();
            return true;
        }
        return false;
    }
    





    
/* REGION - ASTAR STUFF */
    protected boolean lineOfSight(int node1, int node2) {
        int x1 = toTwoDimX(node1);
        int y1 = toTwoDimY(node1);
        int x2 = toTwoDimX(node2);
        int y2 = toTwoDimY(node2);
        return graph.lineOfSight(x1, y1, x2, y2);
    }
    
    protected void maybePostSmooth() {
        if (postSmoothingOn) {
            while(postSmooth());
            /*if (repeatedPostSmooth) {
                while(postSmooth());
            } else {
                postSmooth();
            }*/
        }
    }
    
    private boolean postSmooth() {
        boolean didSomething = false;

        int current = finish;
        while (current != -1) {
            int next = parent(current); // we can skip checking this one as it always has LoS to current.
            if (next != -1) {
                next = parent(next);
                while (next != -1) {
                    if (lineOfSight(current,next)) {
                        setParent(current, next);
                        next = parent(next);
                        didSomething = true;
                    } else {
                        next = -1;
                    }
                }
            }
            
            current = parent(current);
        }
        
        return didSomething;
    }

    private int pathLength() {
        int length = 0;
        int current = finish;
        while (current != -1) {
            current = parent(current);
            length++;
        }
        return length;
    }
    
    
    public int[][] getPath() {
        int length = pathLength();
        int[][] path = new int[length][];
        int current = finish;
        
        int index = length-1;
        while (current != -1) {
            int x = toTwoDimX(current);
            int y = toTwoDimY(current);
            
            path[index] = new int[2];
            path[index][0] = x;
            path[index][1] = y;
            
            index--;
            current = parent(current);
        }
        
        return path;
    }

    protected float getPathLength() {
        int current = finish;
        if (current == -1) return -1;
        
        float pathLength = 0;
        
        int prevX = toTwoDimX(current);
        int prevY = toTwoDimY(current);
        current = parent(current);
        
        while (current != -1) {
            int x = toTwoDimX(current);
            int y = toTwoDimY(current);
            
            pathLength += graph.distance(x, y, prevX, prevY);
            
            current = parent(current);
            prevX = x;
            prevY = y;
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
