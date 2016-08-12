import re

tab = "\t"

BLOCK_TYPE_ARG_VAL = 1
BLOCK_TYPE_TAG_CONT = 2



#given depth of indentitation, function searches for next tag with similar indentitation, that is, sibling tag
#returns length of block for starting start pos
def blockEnd(indentDepthTabs, buf, tagStartPos):
    #a regexp for sequence of tabs followed alphnumeric char
    #reg = '\\t{' + str(indentDepthTabs) + '}[a-zA-Z0-9]'
    reg = '\\n\\t{' + str(indentDepthTabs) + '}[a-zA-Z0-9]'

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


#buf is a complete subtree of a parsed structure, the block from "content start" until "content end", 
#including the indentation before content start - this is critical, because a block is also seen 
#as the content between 2 equaly long indendations 
# tag:
#     content start....
#     atr1 = val1
#     innerTag:
#           innerCtonet
#
#

#     content end

def processBuf(buf, baseIndDepth):
    pos = 0
    htmlOut = ""
    propsMap = {}
    while pos < len(buf):
        blockLen = blockEnd(baseIndDepth, buf, pos + 1)
        if blockLen > 0:
            block = buf[pos:(pos + blockLen + 1)]
            pos = pos + blockLen + 1
        else:
            block = buf[pos:]
            pos = len(buf)
        blockType = extractBlockType(block)
        if blockType == BLOCK_TYPE_ARG_VAL:
            key, val = extractArgVal(block)
            #addArgVal(baseTagBuf, key, val)
            propsMap[key] = val
            continue
        if blockType == BLOCK_TYPE_TAG_CONT:
            tag, bufChild = extractTagContent(block)
            contentasHTML, deepArgsMap = processBuf(bufChild, baseIndDepth + 1)
            openTagHtml, closeTagHtml = builHTMLTags(tag, deepArgsMap)
            indent = indentStr(baseIndDepth)
            htmlOut += "\n" + indent + openTagHtml
            htmlOut += "\n" + indent + tab + contentasHTML
            htmlOut += "\n" + indent + closeTagHtml
            continue 
        
    return htmlOut, propsMap 
        
def  indentStr(depth):
    out = ""
    for i in range (0,depth):
        out += tab
    return out


def builHTMLTags(tag, propsMap):
    #openning tag
    openTag = "<" + tag 
    for prop in propsMap:
        val = propsMap[prop]
        openTag += " " + prop 
        if val:
            openTag += "=" + val
    openTag += ">"
    
    closeTag = "</" + tag+ ">"
    
    openTag = openTag.translate(None, "\n")
    closeTag = closeTag.translate(None, "\n")
    openTag = openTag.translate(None, "\t")
    closeTag = closeTag.translate(None, "\t")
    
    #openTag = re.sub("\\r|\\n", "", openTag)
    #closeTag = re.sub("\\r|\\n", "", closeTag)
    return openTag, closeTag

#baseTagBuf is an html represtaton of a tag <tag atr=val atr2=val2>
#this function injects a key and optional value into the tag
#def addArgVal(baseTagBuf, key, val):
    

#block is assumed to be either in the form key=val, tag <no val> or tag:<newline tab>tagContent        
def extractBlockType(block):
    pos = block.find(":")
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
    return block[0:colPos], block[colPos + 1:]

testReadBlock()
    