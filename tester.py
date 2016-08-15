import goBack
import phtml

orgHtmlFilePath = "ml5smpl_org.html"



def testBackAndForth():
    parsed = phtml.topLevel()
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