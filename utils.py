def readBuffer(filePath):
    """reads given file on to a buffer"""
    buf = ""
    buf += open(filePath, 'rU').read()
    return buf