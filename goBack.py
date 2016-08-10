import re

tab = "\t"

BLOCK_TYPE_ARG_VAL = 1
BLOCK_TYPE_TAG_CONT = 2



#given depth of indentitation, function searches for next tag with similar indentitation, that is, sibling tag
#returns length of block for starting start pos
def blockEnd(indentDepthTabs, buf, tagStartPos):
    #a regexp for sequence of tabs followed alphnumeric char
    #reg = 'r"\\t{' + str(indentDepthTabs) + '}[a-zA-Z0-9]"'
    reg = '\\t{' + str(indentDepthTabs) + '}[a-zA-Z0-9]'
    #reg = '\\t{1}'
    pos = re.search(reg, buf[tagStartPos:-1])
    if pos:
        return pos.start()
    else:
        return -1
    

        
        
def depth(line):
    pos = 0
    
    
def testReadBlock():
    buf = "\n\ttag1: \n \t\ttag1content  \n \t\ttag2: \n \t\t\ttag2content \n \ttag1sibling"  
    print blockEnd(1 , buf, 12)


    
def processBuf(buf, baseIndDepth, baseTagBuf):
    pos = 0
    while pos < buf:
        blockLen = blockEnd(baseIndDepth, buf, pos)
        block = buf[pos:(pos + blockLen)]
        pos = pos + blockLen
        blockType = extractBlockType(block)
        if blockType == BLOCK_TYPE_ARG_VAL:
            key, val = extractArgVal(block)
            addArgVal(baseTagBuf, key, val)
            continue
        if blockType == BLOCK_TYPE_TAG_CONT:
            tag, content == extractTagContent(block)
            openTagHtml, closeTagHtml = builHTMLTags(tag)
            contentasHTML = processBuf(block, baseIndDepth + 1, openTagHtml)
            indent = indentStr(baseIndDepth)
            print indent + openTagHtml
            print contentasHTML
            print indent + closeTagHtml
            
        tag = extractTag(block)
        args = extract
        
#block is assumed to be either in the form key=val, tag <no val> or tag:<newline tab>tagContent        
def extractBlockType(block):
    pos = block.find(">")
    if pos > 0:
        return BLOCK_TYPE_TAG_CONT
    else:
        return BLOCK_TYPE_ARG_VAL
    
def  extractArgVal(block):
    tokens = block.split("=")
    key = tokens[0]
    if len(tokens) > 1:
        val = tokens[1]
    else:
        val = None
    return key, val

#the tag is supposed to be the first line, the content the rest of the block
def extractTagContent(block):
    colPos = block.find(":")
    return block[0:colPos - 1], block[0:colPos + 1, -1]

testReadBlock()
    