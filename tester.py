import goBack
import phtml

orgHtmlFilePath = "ml5smpl_org.html"



def testBackAndForth():
    parsed = phtml.topLevel()
    unParsed = goBack.processBuf(parsed, 0)
    print unParsed[0].expandtabs(5)
    breakpoint = 9
    
    

testBackAndForth()