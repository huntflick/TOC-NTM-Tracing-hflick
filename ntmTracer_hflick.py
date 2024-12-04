import csv
import sys
import time


def main(arguments=sys.argv[1:]):
    try:
        inFile = arguments[0]
        ntm = open(inFile, "r")
        ntm = csv.reader(ntm)
    except IndexError:
        print("Invalid number of arguments")
        exit(1)
    except FileNotFoundError:
        print(f"NTM descriptor file {inFile} not found")
        exit(1)
    
    try:
        inString = arguments[1]
    except IndexError:
        print("Invalid number of arguments")
        exit(1)
    
    try:
        maxDepth = arguments[2]
        arguments = arguments[3:]   # prepare for more input strings
    except IndexError:
        print("Invalid number of arguments")
        exit(1)
    
    while 1:
        output = ntmTrace(ntm, inString, maxDepth)
        print(output)
        try:
            inString = arguments[0]
            arguments = arguments[1:]
        except IndexError:
            break


def ntmTrace(ntm, inString, maxDepth):
    delta = []
    for i, line in enumerate(ntm):  # parse ntm description
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

    depth = 0
    txns = 0
    qcurr = start
    leftHead = ""
    rightHead = inString
    match = 0
    accepted = 0
    rejPath = []
    path = [["", qcurr, rightHead]]

    path, depth, txns = recCheck(path, rejPath, delta, accept, reject, depth, txns)

    # confTree = [
    #             [["", qcurr, rightHead]]
    #             ]
    
    # for level in confTree:
    #     newLevel = []
    #     if not level:
    #         break
    #     for conf in level:
    #         match = 0
    #         qcurr = conf[1]
    #         if qcurr == reject:
    #             pass
    #         leftHead = conf[0]
    #         rightHead = conf[2]
    #         if qcurr == reject:
    #             continue

    #         for rule in delta:
    #             if qcurr == rule[0] and rightHead[0] == rule[1]:
    #                 match = 1
    #                 newq = rule[2]

    #                 if rule[4] == "R":
    #                     newLeft = leftHead + rule[3]
    #                     newRight = rightHead[1:]
    #                     if not newRight:
    #                         newRight = "_"
                    
    #                 if rule[4] == "L":
    #                     newRight = rule[3] + rightHead[1:]
    #                     try:
    #                         newRight = leftHead[-1] + newRight
    #                     except IndexError:
    #                         pass
    #                     try:
    #                         newLeft = leftHead[:-1]
    #                     except IndexError:
    #                         pass

    #                 newConf = [newLeft, newq, newRight]
    #                 newLevel.append(newConf)

    #                 if newq == accept:
    #                     accepted = 1
    #                     break

    #         if accepted:
    #             break

    #         if not match:
    #             newLeft = leftHead + rightHead[0]
    #             newRight = rightHead[1:]
    #             if newRight == "":
    #                 newRight = "_"
    #             newConf = [newLeft, reject, newRight]
    #             newLevel.append(newConf)

    #     if newLevel:
    #         confTree.append(newLevel)
    #     if accepted:
    #         break

    # for level in confTree:
    #     print(level)
    
        
    # return (name, start, accept, reject, delta)

    
    
def recCheck(path, rejPath, delta, accept, reject, depth, txns):
    conf = path[-1]
    match = 0
    qcurr = conf[1]
    leftHead = conf[0]
    rightHead = conf[2]
    newLevel = []

    for rule in delta:
        if qcurr == rule[0] and rightHead[0] == rule[1]:
            match = 1
            newq = rule[2]

            if rule[4] == "R":
                newLeft = leftHead + rule[3]
                newRight = rightHead[1:]
                if not newRight:
                    newRight = "_"
            
            if rule[4] == "L":
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
                return (path, rejPath, depth, txns)
    
    if not match:
        newLeft = leftHead + rightHead[0]
        newRight = rightHead[1:]
        if newRight == "":
            newRight = "_"
        newConf = [newLeft, reject, newRight]
        newRej = path + [newConf]
        if len(newRej) > len(rejPath):
            rejPath = newRej
        return (path, rejPath, depth, txns)
    
    for conf in newLevel:
        newPath = path + [conf]
        res = recCheck(newPath, rejPath, delta, accept, reject, depth, txns)
        print(res)
        path = res[0]
        rejPath = res[1]
        depth = res[2]
        txns = res[3]
















    
    
    # path = init
    # rejPath = []

    # for rule in delta:
    #     eval
    #     add to level
    #     if acc:
    #         return oath, depth, txns
        
    # if not match:
    #     add reject to level
    #     depth+=1
    #     txns+=1
    #     return path, depth, txns

    # for conf in level:
    #     newPath = path.append(conf)
    #     recursiveCall(newPath)
    


    # on execution, run code as above
    # modify to keep a "path" of current execution
    #   on accept, return this path
    #   on reject, check against longest found reject path
    #       if no reject or new reject is longer, safe path
    #       must reset transition counter

    # need to implement depth and transition counters
    #   transition counter must reset and computation must start from beginning
    #           unless find some way to "remember"

    #             head
    #     branch      branch
    # branch  leaf   leaf     branch
    # leaf                        leaf
    
    
    
    
    
    # for level in confTree:

    #     print(level)

    #     if not level:
    #         break
    #     for conf in level:
            
    #         # print(conf)

    #         match = 0
    #         qcurr = conf[1]
    #         leftHead = conf[0]
    #         rightHead = conf[2]
    #         if qcurr == reject:
    #             pass
    #         for rule in delta:
    #             if qcurr == rule[0] and rightHead[0] == rule[1]:    # if curr state head char match
    #                 match = 1
    #                 #print(conf)
    #                 #print(rule)
    #                 newqcurr = rule[2]
    #                 if rule[4] == "R":
    #                     newleftHead = leftHead + rule[3]
    #                     newrightHead = rightHead[1:]
    #                     if not rightHead:
    #                         newrightHead = "_"
    #                 elif rule[4] == "L":
    #                     newrightHead = rule[3] + rightHead[1:]
    #                     try:
    #                         newrightHead = leftHead[-1] + rightHead
    #                     except IndexError:
    #                         pass
    #                     try:
    #                         newleftHead = leftHead[:-1]
    #                     except IndexError:
    #                         pass
    #                 newConf = [newleftHead, newqcurr, newrightHead]
    #                 newLevel.append(newConf)
    #                 if qcurr == accept:
    #                     accepted = 1
    #                     break

    #             #print(confTree)
                
    #         if not match:
    #             qcurr = reject
    #             leftHead = leftHead + rule[3]
    #             rightHead = rightHead[1:]
    #             if not rightHead:
    #                 rightHead = "_"
    #             newConf = [leftHead, qcurr, rightHead]
    #             newLevel.append(newConf)
    #             break
    #         if accepted:
    #             break
    #     if newLevel:        
    #         confTree.append(newLevel)
    #     if accepted:
    #         break
    # print(confTree)
                        


    # return (name, start, accept, reject, delta)


if __name__ == '__main__':
    main()