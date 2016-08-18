import goBack
import phtml
import utils


TEST_INPUT_FILE_REST = "restapi1.xml"

#TEST_INPUT_FILE_HTML = "ml5smpl_org.html"

TEST_INPUT_FILE_HTML = "ml5smpl_orphan_attr.html"

"""

def topLevel(filePath):
   
    outBuf = {}
    outBuf["txt"] = ""
    buf = utils.readBuffer(filePath)
    rootStart = phtml.handlePreRoot(buf, outBuf)
    content, endPos, tagCode = phtml.getTagContent(buf, rootStart)
    outBuf["txt"] += "\n" + "html:"
    phtml.processContent(content, 1, outBuf)
    return outBuf["txt"]
"""



def testBackAndForth():
    buf = utils.readBuffer(TEST_INPUT_FILE_HTML)
    parsed = phtml.translateRawHtml(buf)
    #parsed = topLevel(TESTING_INPUT_HTML1)
    print parsed
    print "-----------and back to:-------------------"
    unParsed = goBack.processBuf(parsed, 0)
    out = unParsed[0]
    print out.expandtabs(5)
    breakpoint = 9
    
def translateXml():
    buf = utils.readBuffer(TEST_INPUT_FILE_REST)
    parsed = phtml.translateXML(buf)
    print parsed
    
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
    
def testSplitHeader():
    #buf = '<user email="paul@peej.co.uk" name="Paul James" href="http://www.peej.co.uk/">'
    buf = '<user email="paul@peej.co.uk" noQProp=noQVal  noValFalg name= "Paul James" href="http://www.peej.co.uk/" >'
    args = phtml.readTagHeader(buf, 0)
    print args

testBackAndForth()
#translateXml()
#testSplitHeader()