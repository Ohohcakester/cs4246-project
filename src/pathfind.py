import subprocess

# look at the comments for the function runPathfinding(mazeName,testcases). This is what you want to call.

# Because some platforms (i.e. windows) don't accept command lengths above 32768 characters. Can set higher if you want it to run faster.
maxQuerySize = None # NO LONGER BEING USED

# Call this function for shortest path computation.
# (calling with a batch of testcases is faster than calling multiple time separately)
# WARNING: Be sure to compile the java files in the pathfinding/ folder first!
# javac *.java   <-- may require java 8. not sure.
#
# Input arguments:
# - mazeName: either 'floor2map' or 'floor18map'
# - testcases: a list of test cases. Each test case is a 4-tuple
#              consisting of the maze coordinates of the start/end
#              points (sx,sy,ex,ey)
# Returns:
# - a list of floats representing the shortest path distances
#              for each of the test cases.
def runPathfinding(mazeName, testcases):
    return runPathfindingChunk(mazeName, testcases)
    """
    testcasesList = [testcases[i:i+maxQuerySize] for i in xrange(0,len(testcases),maxQuerySize)]
    results = []
    for chunk in testcasesList:
        results += runPathfindingChunk(mazeName, chunk)
    #print len(results)
    #print results[:10]
    #print results[-10:]
    return results
    """

def parseTupleWithSpaces(point):
    return ' '.join(map(str,map(int,point)))

def parseShortestPathTuple(t):
    t = t.split('-')
    return int(t[0]), int(t[1]), float(t[2])

def parseOutput(output):
    return map(parseShortestPathTuple, output.split())


def runSingleSourceAllDestinations(mazeName, points):
    args = [mazeName] + list(map(parseTupleWithSpaces,points))
    args = ' '.join(args)

    output = subprocess.check_output('java SingleSourceAllDestinations '+args, cwd='pathfinding', shell=True, close_fds=True)
    return tuple(map(parseOutput, output.split('|')))


def parseTestCase(testcase):
    return '-'.join(map(str,map(int,testcase)))

def runPathfindingChunk(mazeName, testcases):
    args = map(parseTestCase,testcases)
    args = ' '.join(args)

    process = subprocess.Popen('java Compute ' + mazeName, shell=True, cwd='pathfinding', stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
    output = process.communicate(args)

    return list(map(float,output[0].split()))



# Sample / test
if __name__ == '__main__':
    mazeName = 'floor18map'

    # Test All Destinations
    #points = [(15,15), (32,64), (15,16)]
    #print list(map(len,runSingleSourceAllDestinations(mazeName, points)))

    # Test Single Destination
    testcases = [
    (18,20,21,53),
    (18,20,21,54),
    (18,20,21,55),
    (18,20,21,56),
    ]*50000
    print runPathfindingChunk(mazeName, testcases)
    
