import goBack
import phtml
import utils
import unittest


"""
test input files are html or xml file to be translated. the expect files are epected resuts after translation. 
test input file whose name ends with TAB_INDENT have tab indentation, and those ending with WS_INDENT (whitesape 
indentation) have a less strict structure. those with tab indent are needed in order to test reverse translation, 
because reverse translations adds proper tab based indentation according to the html hirarchy, and when comparing 
output with expectation the tabs are also considered. this is not necesserely a good thing, rather a constraint.    

"""

TEST_INPUT_FILE_XML_SIMPLE = "test_input/xml_simple_1.xml" 

TEST_INPUT_FILE_SOAP = "test_input/soap2.xml" 

TEST_INPUT_FILE_HTML_FULL_WS_INDENT = "test_input/html_full.html"

TEST_INPUT_FILE_HTML_FULL_TAB_INDENT = "test_input/html_full_tab.html"

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
        fileIn = TEST_INPUT_FILE_HTML_FULL_WS_INDENT
        f = phtml.translateRawHtml
        fileExpected = TEST_EXPECT_FILE_HTML_FULL_OUT
        self.assertTrue(compareStringWithFileContent(fileIn, fileExpected, f))
    
    
        
        
class ToHtmlTester(unittest.TestCase):
    
    
    #the comparison is with an expected html formatted as expected by the first direction. (such formatting is 
    #not expected on the first direction, but of course must be assumed for testing against output
    #the translation is revirsable up to change in formatting to the html file, as well as some optional closing 
    #tags that would be added 
     
        
    def testTransBackCmp(self):
        fileIn = TEST_EXPECT_FILE_HTML_CMP_OUT
        f = goBack.translageBacktoHtml
        fileExpected = TEST_INPUT_FILE_HTML_CMP_TAB_INDENT
        self.assertTrue(compareStringWithFileContent(fileIn, fileExpected, f))
    
    def testTransBackFull(self):
        fileIn = TEST_EXPECT_FILE_HTML_FULL_OUT
        f = goBack.translageBacktoHtml
        fileExpected = TEST_INPUT_FILE_HTML_FULL_TAB_INDENT
        self.assertTrue(compareStringWithFileContent(fileIn, fileExpected, f))
        


def demoConsoleBackAndForthHTML():
    print "-----------translated:-------------------"
    buf = utils.readBuffer(TEST_INPUT_FILE_HTML_FULL_WS_INDENT)
    trx = phtml.translateRawHtml(buf)
    print trx
    print "-----------and back to html:-------------------"
    unTraxed = goBack.translageBacktoHtml(trx)
    out = unTraxed
    print out.expandtabs(5)
    
def demoConsoleBackAndForthXML():
    print "-----------translated from xml:-------------------"
    buf = utils.readBuffer(TEST_INPUT_FILE_XML_SIMPLE)
    parsed = phtml.translateXML(buf)
    print parsed
    print "-----------and back to xml:-------------------"
    unParsed = goBack.processBuf(parsed, 0)
    out = unParsed[0]
    print out.expandtabs(5)
 
 

#demoConsoleBackAndForthXML()

#demoConsoleBackAndForthHTML()

unittest.main()

