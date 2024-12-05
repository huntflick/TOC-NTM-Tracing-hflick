import csv
import sys


def main(arguments=sys.argv[1:]):
    try:
        inFile = arguments[0]
        ntm = open(inFile, "r")
    except IndexError:
        print("Invalid number of arguments")
        print(f"Usage: python3 {sys.argv[0]} <TESTFILE>.csv <TESTSTRING> <MAXDEPTH> <ADDITIONALSTRINGS . . .>")
        exit(1)
    except FileNotFoundError:
        print(f"NTM descriptor file {inFile} not found")
        exit(1)
    
    try:
        inString = arguments[1]
    except IndexError:
        print("Invalid number of arguments")
        print(f"Usage: python3 {sys.argv[0]} <TESTFILE>.csv <TESTSTRING> <MAXDEPTH> <ADDITIONALSTRINGS . . .>")
        exit(1)
    
    try:
        maxTxns = int(arguments[2])
        arguments = arguments[3:]   # prepare for more input strings
    except IndexError:
        print("Invalid number of arguments")
        print(f"Usage: python3 {sys.argv[0]} <TESTFILE>.csv <TESTSTRING> <MAXDEPTH> <ADDITIONALSTRINGS . . .>")
        exit(1)
    
    while 1:
        ntmTrace(ntm, inString, maxTxns)   # call ntm parser
        try:    # check for additional strings
            inString = arguments[0]
            arguments = arguments[1:]
        except IndexError:
            break



def ntmTrace(ntm, inString, maxTxns):
    delta = []  # rule holder
    data = csv.reader(ntm)
    for i, line in enumerate(data):  # parse ntm description
        if i == 0:
            name = line[0]
        elif i > 0 and i < 4:
            pass
        elif i == 4:
            start = line[0]
        elif i == 5:
            accept = line[0]
        elif i == 6:
            reject = line[0]
        else:
            delta.append(line)
    ntm.seek(0)     # reset file to top

    txns = 0
    numConf = 0
    numLevels = 0
    qcurr = start
    rightHead = inString    # initialize string right of head
    rejPath = []
    path = [["", qcurr, rightHead]]     # initialize path

    path, rejPath, numConf, txns, numLevels = recCheck(path, rejPath, delta, accept, reject, maxTxns, txns, numConf, numLevels)

    # printing results
    print(f"NTM: {name}")
    print(f"Input string: {inString}")
    if path[-1] == "LIMIT EXCEEDED":
        print(f"Execution stopped after {maxTxns} transitions")
    elif path[-1][1] == accept:
        depth = len(path)
        print(f"Accepted in {depth-1} transitions")
        for conf in path:
            print(conf, end=' ')
        print()
        print(f"Explored {txns+1} configurations")      # total number of configs visited (including repeats and start)
    else:
        depth = len(rejPath)
        print(f"Longest rejection path rejected in {depth-1} transitions")
        for conf in rejPath:
            print(conf, end=' ')
        print()
        print(f"Explored {txns+1} configurations")
    print(f"Average nondeterminism: {numConf/numLevels}")   # total number of configs on each txn / number of tree levels
    print()



def recCheck(path, rejPath, delta, accept, reject, maxTxns, txns, numConf, numLevels):  # recursive ntm checker
    conf = path[-1]
    match = 0
    qcurr = conf[1]
    leftHead = conf[0]
    rightHead = conf[2]
    newLevel = []

    if txns >= maxTxns:     # stop execution once max txns hit
        path.append("LIMIT EXCEEDED")
        return (path, rejPath, numConf, txns, numLevels)

    for rule in delta:  # cycle through rules looking for a match
        if qcurr == rule[0] and rightHead[0] == rule[1]:
            txns+= 1
            match = 1
            newq = rule[2]

            if rule[4] == "R":  # move head right
                newLeft = leftHead + rule[3]
                newRight = rightHead[1:]
                if not newRight:
                    newRight = "_"
            
            if rule[4] == "L":  # move head left
                newRight = rule[3] + rightHead[1:]
                try:
                    newRight = leftHead[-1] + newRight
                except IndexError:
                    pass
                try:
                    newLeft = leftHead[:-1]
                except IndexError:
                    pass

            newConf = [newLeft, newq, newRight]
            newLevel.append(newConf)

            if newq == accept:
                path.append(newConf)
                return (path, rejPath, numConf, txns, numLevels)
    
    if not match:   # go to reject
        txns+= 1
        try:
            newRight = leftHead[-1] + rightHead
        except IndexError:
            newRight = rightHead
        newLeft = leftHead[:-1]
        newConf = [newLeft, reject, newRight]
        path.append(newConf)
        newRej = path
        if len(newRej) > len(rejPath):  # determine longer reject path
            rejPath = newRej
        return (path, rejPath, numConf, txns, numLevels)
    
    numConf+= len(newLevel) - 1
    numLevels+= 1
    for conf in newLevel:   # pick next configuration to visit
        if path[-1][1] == reject:   # "undo" last transitions to reject
            newPath = path[:-2] + [conf]
        else:
            newPath = path + [conf]
        res = recCheck(newPath, rejPath, delta, accept, reject, maxTxns, txns, numConf, numLevels)
        retPath = res[0]
        rejPath = res[1]
        numConf = res[2]
        txns = res[3]
        if retPath[-1][1] == accept:    # return if accepted
            return (retPath, rejPath, numConf, txns, numLevels)
    
    return (retPath, rejPath, numConf, txns, numLevels)



if __name__ == '__main__':
    main()