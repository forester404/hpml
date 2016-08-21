import goBack
import phtml
import utils
import unittest




TEST_INPUT_FILE_XML_SIMPLE = "test_input/xml_simple_1.xml" 

TEST_INPUT_FILE_SOAP = "test_input/soap2.xml" 

TEST_INPUT_FILE_HTML_FULL = "test_input/html_full.html"

TEST_INPUT_FILE_HTML_CMP_WS_INDENT = "test_input/html_compact_ws_ind.html"

TEST_INPUT_FILE_HTML_CMP_TAB_INDENT = "test_input/html_compact_tab_ind.html"

TEST_EXPECT_FILE_HTML_CMP_OUT = "test_input/expect_out_from_html_cmp.pig"

TEST_EXPECT_FILE_HTML_FULL_OUT = "test_input/expected_out_from_html_full.pig"


def compareStringWithFileContent(fileIn, fileExpected, processFunction):  
    """
    reads content of input, processes it with given funtion, then compares it with content 
    read from expected result file 
    """
    inContent = utils.readBuffer(fileIn) 
    expected = utils.readBuffer(fileExpected)
    processed = processFunction(inContent)        
    return processed.strip() == expected.strip()
    


class FromHtmlTester(unittest.TestCase):
    def testtest(self):
        assert True
    
    
    def testTranslHTMLCompactTagInd(self):
        fileIn = TEST_INPUT_FILE_HTML_CMP_TAB_INDENT
        f = phtml.translateRawHtml
        fileExpected = TEST_EXPECT_FILE_HTML_CMP_OUT
        self.assertTrue(compareStringWithFileContent(fileIn, fileExpected, f))
        
    def testTranslHTMLCompactWsInd(self):
        fileIn = TEST_INPUT_FILE_HTML_CMP_WS_INDENT
        f = phtml.translateRawHtml
        fileExpected = TEST_EXPECT_FILE_HTML_CMP_OUT
        self.assertTrue(compareStringWithFileContent(fileIn, fileExpected, f))
    
    def testTranslHTMLFull(self):
        fileIn = TEST_INPUT_FILE_HTML_FULL
        f = phtml.translateRawHtml
        fileExpected = TEST_EXPECT_FILE_HTML_FULL_OUT
        self.assertTrue(compareStringWithFileContent(fileIn, fileExpected, f))
    
    
        
        
class ToHtmlTester(unittest.TestCase):
    
    
    #the comparison is with an expected html formatted as expected by the first direction. (such formatting is 
    #not expected on the first direction, but of course must be assumed for testing against output
    #the translation is revirsable up to change in formatting to the html file, as well as some optional closing 
    #tags that would be added 
     
        
    def testTransBack2(self):
        fileIn = TEST_EXPECT_FILE_HTML_CMP_OUT
        f = goBack.translageBacktoHtml
        fileExpected = TEST_INPUT_FILE_HTML_CMP_TAB_INDENT
        self.assertTrue(compareStringWithFileContent(fileIn, fileExpected, f))
        
        
    


def testBackAndForth():
    buf = utils.readBuffer(TEST_INPUT_FILE_HTML_FULL)
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


def serExpectedFull():
    
    
    inContent = utils.readBuffer(TEST_INPUT_FILE_HTML_FULL)
    trx = phtml.translateRawHtml(inContent)
    text_file = open("temp_ser.txt", "w")
    text_file.write(trx)
    text_file.close()   
   
    
def testReadBlock():
    buf = "\n\ttag1: \n \t\ttag1content  \n \t\ttag2: \n \t\t\ttag2content \n \ttag1sibling"  
    print goBack.blockEnd(1 , buf, 12)

testBackAndForth()
#translateXml()
#testSplitHeader()
#testSplitHeadSoap()


#unittest.main()

#serExpectedFull()