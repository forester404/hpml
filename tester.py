import goBack
import phtml
import utils

TESTING_INPUT_HTML1 = "ml5smpl_org.html"

filePath = "ml5smpl_org.html"

def topLevel(filePath):
    """
    reads an html file into a buffer, parses it to cleanView 
    """
    outBuf = {}
    outBuf["txt"] = ""
    buf = utils.readBuffer(filePath)
    rootStart = phtml.handlePreRoot(buf, outBuf)
    content, endPos, tagCode = phtml.getTagContent(buf, rootStart)
    outBuf["txt"] += "\n" + "html:"
    phtml.processContent(content, 1, outBuf)
    return outBuf["txt"]

def testBackAndForth():
    parsed = topLevel(TESTING_INPUT_HTML1)
    print parsed
    print "-----------and back to:-------------------"
    unParsed = goBack.processBuf(parsed, 0)
    out = unParsed[0]
    print out.expandtabs(5)
    breakpoint = 9
    
def testCountTabs():
    line = "\n\n\t\t\tand that is it"
    print goBack.countTagbsAtPrefix(line)   
    
def testRecongnizeIdentBlock():
    block = "\ttag:\n\t\tcont"
    print goBack.isBlockContainingInnerIndent(block)
    block = "\ttag:\n\t\tc=ont"
    print goBack.isBlockContainingInnerIndent(block)
    block = "prop=34"
    print goBack.isBlockContainingInnerIndent(block)
    block = "simpleContentLine1\nsimpleContentLine2\nsimpleContentLine3"
    print goBack.isBlockContainingInnerIndent(block)
    block = "\ttag:\ntcont"
    print goBack.isBlockContainingInnerIndent(block)
    

testBackAndForth()

#testRecongnizeIdentBlock()
#testCountTabs()