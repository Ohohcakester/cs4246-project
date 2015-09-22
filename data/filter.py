import datetime

filterHeaders = [
'SNAPSHOT_TIMESTAMP',
'TAG_ID',
'AREA_ID',
'X',
'Y',
'Z',
]

def sortBy(rows, field):
    index = filterHeaders.index(field)
    rows.sort(key=lambda v : v[index])
    
def get(outputMatrix, field):
    return outputMatrix[filterHeaders.index(field)]
    
def mapField(fun, outputMatrix, field):
    index = filterHeaders.index(field)
    outputMatrix[index] = list(map(fun, outputMatrix[index]))

def filterRows(fun, rows):
    return list(filter(fun, rows))
    
def hasAllEntries(li):
    return '' not in li
    
def convertDateTime(d):
    return unix_time(datetime.datetime.strptime(d, '%m/%d/%Y %H:%M:%S %p'))
    
def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0
    
def process(headers, lines):
    outputMatrix = getOutputMatrix(headers, lines)
    mapField(convertDateTime, outputMatrix, 'SNAPSHOT_TIMESTAMP')
    #mapField(int, outputMatrix, 'USERID')
    #mapField(float, outputMatrix, 'LONGITUDE')
    #mapField(float, outputMatrix, 'LATITUDE')
    #mapField(int, outputMatrix, 'TIMESTAMP')
    #minTime = min(get(outputMatrix,'TIMESTAMP'))
    #x1 = min(get(outputMatrix,'LONGITUDE'))
    #x2 = max(get(outputMatrix,'LONGITUDE'))
    #y1 = min(get(outputMatrix,'LATITUDE'))
    #y2 = max(get(outputMatrix,'LATITUDE'))
    #mapField(lambda x : x-minTime, outputMatrix, 'TIMESTAMP')
    #mapField(lambda x : x-x1, outputMatrix, 'LONGITUDE')
    #mapField(lambda x : x-y1, outputMatrix, 'LATITUDE')
    
    
    
    outputMatrix = transposeMatrix(outputMatrix)
    #csvPrint(filterHeaders)
    #print(' '.join(map(str,[x2-x1,y2-y1])))
    
    sortBy(outputMatrix, 'SNAPSHOT_TIMESTAMP')
    #sortBy(outputMatrix, 'TAG_ID')
    outputMatrix = filterRows(hasAllEntries, outputMatrix)
    
    currTag = -1
    f = open('conf/LOL.csv', 'w+')
    for row in outputMatrix:
        if currTag != row[1]:
            currTag = row[1]
            #if f != None:
                #f.close()
                #f = None
            #f = open('conf/' + currTag + '.csv', 'w+')
            #filePrint(headers, f)
        filePrint(row, f)
        
    if f != None:
        f.close()
        f = None
        
    #s = list(set(map(lambda v : tuple(map(int,v[0:2])), outputMatrix)))
    #s.sort()
    #for v in s:
        #print(v)
        
    
    
def csvPrint(li):
    print(','.join(map(str,li)))
    
def filePrint(li, f):
    f.write(','.join(map(str,li)))
    f.write('\n')
        
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
    headers = raw_input().split(',')
    
    lines = []
    s = raw_input()
    while s != None:
        lines.append(s.split(','))
        try:
            s = raw_input()
        except:
            s = None
            
    process(headers, lines)
            
            
if __name__ == '__main__':
    main()