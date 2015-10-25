import subprocess

# Because some platforms (i.e. windows) don't accept command lengths above 32768 characters. Can set higher if you want it to run faster.
maxQuerySize = 2500

def parseTestCase(testcase):
    return '-'.join(map(str,map(int,testcase)))

def runPathfindingChunk(mazeName, testcases):
    args = [mazeName] + list(map(parseTestCase,testcases))
    args = ' '.join(args)

    output = subprocess.check_output('java Compute '+args, cwd='pathfinding', shell=False)
    return list(map(float,output.split()))
    
def runPathfinding(mazeName, testcases):
    testcasesList = [testcases[i:i+maxQuerySize] for i in xrange(0,len(testcases),maxQuerySize)]
    results = []
    for chunk in testcasesList:
        results += runPathfindingChunk(mazeName, chunk)
    print len(results)
    print results[:10]
    print results[-10:]
    return results
    
if __name__ == '__main__':
    mazeName = 'floor18map'
    testcases = [
    (18,20,21,53),
    (18,20,21,54),
    (18,20,21,55),
    (18,20,21,56),
    ]*5000
    runPathfinding(mazeName, testcases)
    