import pygame
import sys

def formatMaze(w,h,rows):
    outputstr = ' '.join(map(str,[w,h])) + '\n'
    strrows = map(lambda row : ' '.join(map(str,row)), rows)
    return outputstr + '\n'.join(strrows)

def toBinaryColour(b):
    if b <= 127: return 1
    return 0
    
def loadMaze(imageFile):
    s = pygame.image.load(imageFile)
    w = s.get_width()
    h = s.get_height()
    colourvalues = pygame.image.tostring(s, 'RGB')
    rows = []
    for y in range(0,h):
        row = []
        for x in range(0,w):
            row.append(toBinaryColour(colourvalues[3*(y*w + x)]))
        rows.append(row)
    
    return formatMaze(w,h,rows)
    
def setExtToTxt(fileName):
    return fileName[:fileName.rfind('.')]+'.txt'
    
if __name__ == '__main__':
    for fileName in sys.argv[1:]:
        s = loadMaze(fileName)
        f = open(setExtToTxt(fileName), 'w+')
        f.write(s)
        f.close()
    