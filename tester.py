import goBack
import phtml
import utils
import unittest




TEST_INPUT_FILE_XML_SIMPLE = "test_input/xml_simple_1.xml" 

TEST_INPUT_FILE_SOAP = "test_input/soap2.xml" 

TEST_INPUT_FILE_HTML = "test_input/ml5smpl_org.html"


                 

class FromHtmlTester(unittest.TestCase):
    def testtest(self):
        assert True
        
    def testTranslHTML(self):
        src = utils.readBuffer("test_input/html_src_1.html")
        expected = utils.readBuffer("test_input/expct_trx_1.pig")
        trx = phtml.translateRawHtml(src)
        self.assertEqual(trx.strip(), expected.strip() )
       
        

        
        
class ToHtmlTester(unittest.TestCase):
    def testtest(self):
        assert True

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
#-------------------------------------------TESTS-----------------------------------------
"""    
def testReadTag():
    buffer = readBuffer()
    print(readTag(buffer, 0)).expandtabs(TAB_WIDTH)
    

def testSimpleStringOps():
    tag = "tag"
    print ("</" + tag + ">").expandtabs(TAB_WIDTH)
    
def testFindFrom():
    print ("abxxab".find("abrrr", 3)).expandtabs(TAB_WIDTH)
    
    

    
    
def testFindEndOfRoot():
    buffer = readBuffer()
    closingTagPos = closingTagIndex(buffer, 333)
    print closingTagPos
        
def testGetContent():
    buffer = readBuffer()
    content = getTagContent(buffer, 0)
    print "**content :*****" 
    print content 
    

def testReadHeader ():    
    print readTagHeader ('<a href="hello" key2=val2 disabled>', 0)

    
def testPrintArgs():
    args={}
    args["img"] = "http blah blavh blag"
    args["keyn"] = "valn"
    outputArgsMap(2, args)
    
def testReadArgsLen():
    buf = " <body bgcolor=white>"
    args, len = readTagHeader (buf, 0)
    print len

def testRe():
    #m = re.search('(?<=abc)def', 'abcdef')
    m = re.search('[a-zA-Z0-9_]', '  d  ')
    print m is None
    """


def testBackAndForth():
    buf = utils.readBuffer(TEST_INPUT_FILE_HTML)
    trx = phtml.translateRawHtml(buf)
    print trx
    print "-----------and back to:-------------------"
    unTraxed = goBack.translageBacktoHtml(trx)
    out = unTraxed
    print out.expandtabs(5)
    
def translateXml():
    #ok
    buf = utils.readBuffer(TEST_INPUT_FILE_XML_SIMPLE)
    
    #not ok
    #buf = utils.readBuffer(TEST_INPUT_FILE_SOAP)
    parsed = phtml.translateXML(buf)
    print parsed
    print "-----------and back to:-------------------"
    unParsed = goBack.processBuf(parsed, 0)
    out = unParsed[0]
    print out.expandtabs(5)
    
def testCountTabs():
    line = "\n\n\t\t\tand that is it"
    print goBack.countLeadingTags(line)   
    
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
    
    
def  testSplitHeadSoap():
    buf = """<soap11:Envelope  
  xmlns="urn:GoogleSearch" 
  xmlns:google="urn:GoogleSearch"
  xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:soap11="http://schemas.xmlsoap.org/soap/envelope/">"""
    args = phtml.readTagHeader(buf, 0)
    print args
    
    
def testReadBlock():
    buf = "\n\ttag1: \n \t\ttag1content  \n \t\ttag2: \n \t\t\ttag2content \n \ttag1sibling"  
    print goBack.blockEnd(1 , buf, 12)

#testBackAndForth()
#translateXml()
#testSplitHeader()
#testSplitHeadSoap()


unittest.main()