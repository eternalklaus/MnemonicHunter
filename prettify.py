#!/usr/bin/python
#-*- coding: utf-8 -*-

PATTERN1    = [] # REG + REGREF
PATTERN2    = [] # REGREF + REG
PATTERN3    = [] # IMM + REGREF
PATTERN4    = [] # REGREF + IMM
PATTERN_ETC = []

def intel2att(line):
    line = line.replace(',',' ') # what if ' ' is '  '? splitted as 2? 
    line = line.replace('  ',' ')
    linesplit = line.split(' ')
    if len(linesplit) is 3:
        line = linesplit[0] + ' ' + linesplit[2] + ' ' + linesplit[1]
    return line    


def lowercase(line):
    return line.lower()

def my_mnemonify(line):
    line = line.replace('r/m32', 'REGREF')
    line = line.replace(' r32', ' REG')
    line = line.replace('imm32', 'IMM')
    line = line.replace('imm8', 'IMM')

    linesplit = line.split(' ')
    line = ''
    for i in xrange(len(linesplit)):
        line += '\''
        if i is 0:
            line += ' '
        line += linesplit[i]
        line += '\''
        line += ' + '
    return line[:-2]

def collectpattern(line):
    tmp = line
    tmp = tmp.replace('\'','')
    tmp = tmp.replace(' ','')
    tmp = tmp.split('+')
    
    if len(tmp) is 3:
        if   tmp[1] == 'REG' and tmp[2] == 'REGREF':
            PATTERN1.append(line)
        elif tmp[1] == 'REGREF' and tmp[2] == 'REG':
            PATTERN2.append(line)
        elif tmp[1] == 'IMM' and tmp[2] == 'REGREF':
            PATTERN3.append(line)
        elif tmp[1] == 'REGREF' and tmp[2] == 'IMM':
            PATTERN4.append(line)
    else:
        PATTERN_ETC.append(line)


def printpatterns():
    print 'REG + REGREF'
    for l in PATTERN1:
        print l
    print ''

    print 'REGREF + REG'
    for l in PATTERN2:
        print l
    print ''

    print 'IMM + REGREF'
    for l in PATTERN3:
        print l
    print ''

    print 'REGREF + IMM'
    for l in PATTERN4:
        print l
    print ''

    print 'ETC.....'
    for l in PATTERN_ETC:
        print l
    print ''

if __name__ == '__main__':

    f = open('res')

    while True:
        line = f.readline()
        if not line: break


        line = line.strip()
        line = lowercase(line)
     
        line = intel2att(line) 
        line = my_mnemonify(line)

        collectpattern(line) 
    
        

    print '______________________'
    printpatterns()

    f.close()

