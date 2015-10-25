import datetime

def parse(s):
    original = s
    unixTime = convertDateTime(s)
    convertBack = fromUnixTime(unixTime)
    print '====\n' + '\n'.join(map(str,(original,unixTime,convertBack)))
    
def fromUnixTime(timestamp):
    return datetime.datetime.utcfromtimestamp(int(timestamp)).strftime('%m/%d/%Y %I:%M:%S %p')
    
def convertDateTime(d):
    return int(unix_time(datetime.datetime.strptime(d, '%m/%d/%Y %I:%M:%S %p')))
    
def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

    
if __name__ == '__main__':
    s = raw_input()
    while s != None:
        parse(s)
        try:
            s = raw_input()
        except:
            s = None