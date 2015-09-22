
filterHeaders = [
'USERID',
'LONGITUDE',
'LATITUDE',
'FLOOR',
'TIMESTAMP',
]

def sortBy(rows, field):
    index = filterHeaders.index(field)
    rows.sort(key=lambda v : v[index])
    
def get(outputMatrix, field):
    return outputMatrix[filterHeaders.index(field)]
    
def mapField(fun, outputMatrix, field):
    index = filterHeaders.index(field)
    outputMatrix[index] = list(map(fun, outputMatrix[index]))

def process(headers, lines):
    outputMatrix = getOutputMatrix(headers, lines)
    mapField(int, outputMatrix, 'USERID')
    mapField(float, outputMatrix, 'LONGITUDE')
    mapField(float, outputMatrix, 'LATITUDE')
    mapField(int, outputMatrix, 'TIMESTAMP')
    minTime = min(get(outputMatrix,'TIMESTAMP'))
    x1 = min(get(outputMatrix,'LONGITUDE'))
    x2 = max(get(outputMatrix,'LONGITUDE'))
    y1 = min(get(outputMatrix,'LATITUDE'))
    y2 = max(get(outputMatrix,'LATITUDE'))
    #mapField(lambda x : x-minTime, outputMatrix, 'TIMESTAMP')
    #mapField(lambda x : x-x1, outputMatrix, 'LONGITUDE')
    #mapField(lambda x : x-y1, outputMatrix, 'LATITUDE')
    
    outputMatrix = transposeMatrix(outputMatrix)
    csvPrint(filterHeaders)
    #print(' '.join(map(str,[x2-x1,y2-y1])))
    
    sortBy(outputMatrix, 'TIMESTAMP')
    sortBy(outputMatrix, 'USERID')
    for row in outputMatrix:
        csvPrint(row)
    
def csvPrint(li):
    print(','.join(map(str,li)))
        
def transposeMatrix(lists):
    return list(map(list, zip(*lists)))

def getOutputMatrix(headers, lines):
    d = dict(zip(headers,range(0,len(headers))))
    outputMatrix = []
    for key in filterHeaders:
        if key not in d:
            print('Key not found: ' + str(key))
            quit()
        index = d[key]
        li = list(map(lambda arr : arr[index], lines))
        outputMatrix.append(li)
    return outputMatrix

def main():
    headers = input().split(',')

    lines = []
    s = input()
    while s != None:
        lines.append(s.split(','))
        try:
            s = input()
        except:
            s = None
            
    process(headers, lines)
            
            
if __name__ == '__main__':
    main()