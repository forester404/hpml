import goBack
import phtml

orgHtmlFilePath = "ml5smpl_org.html"



def testBackAndForth():
    parsed = phtml.topLevel()
    unParsed = goBack.processBuf(parsed, 0)
    out = unParsed[0]
    print out.expandtabs(5)
    breakpoint = 9
    
    

testBackAndForth()