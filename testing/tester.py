import sys
sys.path.insert(0, "../src/")

import goBack
import phtml
import utils
import unittest

"""
testing module for translations on both directions 
"""
#TODO - testing of low level functionality of helping funtions is not implemnted
#TODO - testing error handling is not implemented 


"""
test input files are html or xml file to be translated. the expect files are expected results after translation. 
test input file whose name ends with TAB_INDENT have tab indentation, and those ending with WS_INDENT (whitespace 
indentation) have a less strict structure. those with tab indentation are needed in order to test reverse translation, 
because reverse translations adds proper tab based indentation according to the html hirarchy, and when comparing 
output with expectation indentation is also considered, even for html where it is not really a part of the syntax. 
this is a constraint, a comparison of html content without considering the indentation could have possibly be more 
suitable     

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
    reads content of input, processes it with given function, then compares it with content 
    read from expected result file 
    """
    inContent = utils.readBuffer(fileIn) 
    expected = utils.readBuffer(fileExpected)
    processed = processFunction(inContent)        
    return processed.strip() == expected.strip()
    


class FromHtmlTester(unittest.TestCase):
    """
    contains tests for translation from html to page19
    all tests consist of reading an input html file, processing it and comparing with expected result 
    """ 
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
    
    """
    contains tests of translation from  page19 to html (tran)
    all tests consist of reading a page19 file, 
    , processing it and comparing with expected result 
    """ 
        
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
    """
    this is a demo that prints on console out put of translation in both directions 
    """
    print "-----------translated:-------------------"
    buf = utils.readBuffer(TEST_INPUT_FILE_HTML_FULL_WS_INDENT)
    trx = phtml.translateRawHtml(buf)
    print trx
    print "-----------and back to html:-------------------"
    unTraxed = goBack.translageBacktoHtml(trx)
    out = unTraxed
    print out.expandtabs(5)
    
def demoConsoleBackAndForthXML():
    """
    this is a demo that prints on console out put of translation in both directions 
    """
    print "-----------translated from xml:-------------------"
    buf = utils.readBuffer(TEST_INPUT_FILE_XML_SIMPLE)
    parsed = phtml.translateXML(buf)
    print parsed
    print "-----------and back to xml:-------------------"
    unParsed = goBack.processBuf(parsed, 0)
    out = unParsed[0]
    print out.expandtabs(5)
 
 
#uncomment to run demo of html translate
demoConsoleBackAndForthHTML()

#uncomment to run demo of xml translate
#demoConsoleBackAndForthXML()

#uncomment to run the tests
#unittest.main()

