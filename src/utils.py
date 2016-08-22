TAB = "\t"

def readBuffer(filePath):
    """reads given file on to a buffer"""
    buf = ""
    buf += open(filePath, 'rU').read()
    return buf


def bldInd(numberOfTabs):
    """builds indentation string out of tab chars"""
    out = ""
    for i in range(0,numberOfTabs):
        out += TAB
    return out