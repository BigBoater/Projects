import sys

TOTAL_DISKS = 6

TOWERS = { 'A': list(reversed(range(1, TOTAL_DISKS+1))),
           'B': [],
           'C' : []}

def printDisk(diskNum):
    emptySpace = ' ' * (TOTAL_DISKS - diskNum)
    if diskNum == 0:
        sys.stdout.write(emptySpace + '||' + emptySpace)
    else:
        diskSpace = '@' * diskNum
        diskNumLabel = str(diskNum).rjust(2, '_')
        sys.stdout.write(emptySpace + diskSpace + diskNumLabel + diskSpace + emptySpace)

def printTowers():
    for level in range(TOTAL_DISKS, -1, -1):
        for tower in (TOWERS['A'], TOWERS['B'], TOWERS['C']):
            if level >= len(tower):
                printDisk(0)
            else:
                printDisk(tower[level])
        sys.stdout.write('\n')
    emptySpace = ' ' * (TOTAL_DISKS)
    print('%s A%s%s B%s%s C\n' % (emptySpace, emptySpace, emptySpace, emptySpace, emptySpace))

def moveOneDisk(startTower, endTower):
    disk = TOWERS[startTower].pop()
    TOWERS[endTower].append(disk)

def solve(numberOfDisks, startTower, endTower, tempTower):
    if numberOfDisks == 1:
        moveOneDisk(startTower, endTower)
        printTowers()
        return
    else:
        solve(numberOfDisks - 1, startTower, tempTower, endTower)
        moveOneDisk(startTower, endTower)
        printTowers()
        solve(numberOfDisks - 1, tempTower, endTower, startTower)
        return

printTowers()
solve(TOTAL_DISKS, 'A', 'B', 'C')
