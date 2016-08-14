import re

#filePath = "sample2.html"
#filePath = "ml5smpl.html"
#filePath = "ml5smpl_no_comments.html"
filePath = "ml5smpl_org.html"


TAG_CLOSING = 1
TAG_OPENNING = 2
TAG_NONE = 3	

TAB_WIDTH = 5
#tab = "     "
tab = "\t"
#tab = "tab "


CLOSING_TAG_NONE = 1
CLOSING_TAG_NORMAL = 2
#dbg_file = open("dbg.txt", "w")

def topLevel():
	#dbg_file = open("dbg.txt", "w")
	outBuf = {}
	outBuf["txt"] = ""
	buf = readBuffer()
	
	rootStart = handlePreRoot(buf, outBuf)
	content, endPos, tagCode = getTagContent(buf, rootStart)
	
	
	
	#processContent(content, 0)
	#print "html:"
	outBuf["txt"] += "\n" + "html:"
	processContent(content, 1, outBuf)
	return outBuf["txt"]
	
	#dbg_file.close()
#handles the content of the CONTENT element, return position of HTML element opening <
def handlePreRoot(buf, outBuf):
	htmlPos = buf.find("<html", 0)
	contentInfoIndex = buf.find("<!DOCTYPE", 0)
	if contentInfoIndex == -1:
		return htmlPos
	contentStartPos = contentInfoIndex + len("<!DOCTYPE") + 1
	closingPos = buf.find(">", contentStartPos)
	#print "!DOCTYPE:"
	outBuf["txt"] += "\n" + "!DOCTYPE:"
	#print (tab + buf[contentStartPos : closingPos]).expandtabs(TAB_WIDTH)
	#outBuf["txt"] += "\n" + (tab + buf[contentStartPos : closingPos]).expandtabs(TAB_WIDTH)
	outBuf["txt"] += "\n" + (tab + buf[contentStartPos : closingPos])
	return htmlPos





def processContent(content, indentInTabs, outBuf):

	
	if not content:
		return
	
	i = 0
	while i < len(content):
		strContent = {}
		nextTagPos = nextStargTag(content, i, strContent)
		
		
		if strContent["txt"]:
			printSimpleContent (indentInTabs, strContent, outBuf)
		
		
		#if all inner complex elments processed (also true if content was just primitives)
		if nextTagPos == -1:
			return
		
		if itsAComment(content, nextTagPos):
			commentBlockLen = handleComment(content, indentInTabs, nextTagPos, outBuf)
			i = i + commentBlockLen
		#else, it's a normal tag 
		else:
			#print tag
			tag = readTag(content, nextTagPos)
			indent = ""
			for k in range (0,indentInTabs):
				indent += tab
			#print (indent + tag + ":").expandtabs(TAB_WIDTH)
			#outBuf["txt"] += "\n" + (indent + tag + ":").expandtabs(TAB_WIDTH)
			outBuf["txt"] += "\n" + (indent + tag + ":")
			
			#print tag args
			args, tagWargsLen = readTagHeader (content, nextTagPos)
			printArgsMap(indentInTabs + 1, args, outBuf)
			
			#process tag nested content
			tagContent, endTagPos, tagCode = getTagContent(content, nextTagPos)
			if tagCode == CLOSING_TAG_NORMAL:
				processContent(tagContent, indentInTabs + 1, outBuf)
			
			i = endTagPos 
			
			#if start tag had no matching closing tag, we just #need to consume it. if it had, the pointer would #point at the begining of closing tag, and we need #to consume it
			
			if tagCode == CLOSING_TAG_NONE:
				i = i + tagWargsLen + len(">")	
			else:
				i = i + len("/>") + len(tag) + len(">")


#parses and outputs a comment, returns the complet size of the block including tags
def handleComment(buf, indentInTabs, startOfOPenTagPos, outBuf):
	ind = bldInd(indentInTabs)
	pos = startOfOPenTagPos
	output = ""
	startCont = pos + len("<!--")
	#startCont = pos + len("!--")
	endCont = buf.find("-->")
	content = buf[startCont:endCont]
	contentLines = content.split('\n')
	output += "\n" + ind + "#:"
	for line in contentLines:
		output +=  "\n" + ind + tab + line
	
	#output +=  "\n" + ind + tab + content
	#print output.expandtabs(TAB_WIDTH)
	#outBuf["txt"] += output.expandtabs(TAB_WIDTH)
	outBuf["txt"] += output
	
	return endCont + len("-->") - startOfOPenTagPos
	
	

def bldInd(numberOfTabs):
	out = ""
	for i in range(0,numberOfTabs):
		out += tab
	return out

def itsAComment(buf, nextTagPos):
	#for it to be a comment, it must at least the length of openneing and closing tags away from end of buf
	if len(buf) < nextTagPos + 6:
		return False
	#true iff matches open tag
	openTagMatch = buf[nextTagPos + 1 : nextTagPos + 4] == "!--"
	return openTagMatch

def readBuffer():
	#buffer = "Read buffer:\n"
	buf = ""
	buf += open(filePath, 'rU').read()
	return buf

"""
def printSimpleContent (indentDepth, simpleConent, outBuf):
	
	#if string is only non alphanumeric chars - abort
	m = re.search('[a-zA-Z0-9_]', simpleConent["txt"])
	if m is None:
		return
	
	ind = ""
	line = simpleConent["txt"]
	line = line.strip('\n')
	line = line.strip('\t')
	line = line.strip("\r\n")
	line = line.strip('\r')
	#\r\n
	for i in range (0, indentDepth):
		ind += tab
	if line:	
		print (ind + line).expandtabs(TAB_WIDTH)
		#outBuf["txt"] += "\n" + (ind + line).expandtabs(TAB_WIDTH)
		outBuf["txt"] += "\n" + (ind + line)
"""		
def printSimpleContent (indentDepth, simpleConent, outBuf):
	
	#if string is only non alphanumeric chars - abort
	m = re.search('[a-zA-Z0-9_]', simpleConent["txt"])
	if m is None:
		return
	
	ind = ""
	buf = simpleConent["txt"]
	#line = line.strip('\n')
	buf = buf.strip('\t')
	#line = line.strip("\r\n")
	buf = buf.strip('\r')
	#\r\n
	
	for i in range (0, indentDepth):
		ind += tab
	lines = buf.split("\n")
	#print "\n" + ind + "leaf:"
	outBuf["txt"] += "\n" + ind + "leaf:"
	for line in lines:
		if line:
			line = line.strip()
			out = "\n" + ind + tab + line
			#print (out).expandtabs(TAB_WIDTH)
			#outBuf["txt"] += "\n" + (ind + line).expandtabs(TAB_WIDTH)
			outBuf["txt"] += out
	
	
	
def nextStargTag(buffer, index, strContent):
	contBuf = ""
	while index < len(buffer):
		if buffer[index] == '<':
			#if it's a comment 
			"""if index < len(buffer) - 3 and buffer[index + 1 : index + 4] == "!--":
				commentEndIndex = buffer.find("-->") + 3
				contBuf += buffer[index : commentEndIndex] 
				index = commentEndIndex
			else:	
				strContent["txt"] = contBuf
				return index
			"""
			strContent["txt"] = contBuf
			return index
		contBuf += buffer[index]
		index = index + 1
		
	strContent["txt"] = contBuf
	return -1
	
	
#returnn the index to beginning of closing tag, given start index, the index of the opening "<" in openening tag
def closingTagIndex(buffer, startIndex):
	nextTagStart = startIndex
	tagStack = []
	tag = readTag(buffer, startIndex)
	#endTag = "</" + tag + ">"
	
	while nextTagStart < len(buffer) and nextTagStart != -1:
		nextTagStart = buffer.find(tag, nextTagStart + 1)
		#closing tag - remove the last openneing tag, if the stack is then empty we found we were looking for 
		if nextTagStart == -1:
			return -1
		ttype = tagType(buffer, nextTagStart) 
		if ttype == TAG_CLOSING:
			if len(tagStack) == 1:
				#found it
				return nextTagStart
			else:
				del tagStack[-1]
		#else, if opening tag
		else:
			if ttype == TAG_OPENNING: 
				tagStack.append(tag)
		
	return -1
	#raise ValueError("buffer is not valid html") 
	
#given a location of starting of a tab(1st char), returns true iff the tag is closing one 
#the location is assumed to be in a tag, either openning or closing one 
def tagType(buffer, index):
	if index < 1:
		raise ValueError("tagType, index must have value > 0")
	#if buffer[index - 1] == "/":
	if buffer[index - 2 : index ] == "</":
		return TAG_CLOSING
	if buffer[index - 1] == "<":
		return TAG_OPENNING
	return TAG_NONE
	#raise ValueError("input is not first char of openning or closing tag for {}".format(buffer[index - 1:index])) 



#start index is the index of the opening "<"
def readTag(buffer, startingIndex):
	tag = ""
	i = startingIndex + 1 
	while buffer[i] != ">" and buffer[i] != " ":
		tag += buffer[i]
		i = i + 1
	return tag

#start index is the index of the opening "<"
#ret atrb - map of attrb an vals
#ret totLen = total length of entire openning tag and args, not 
#including brakets 
def readTagHeader (buffer, startingIndex):
	atrbs  = {}
	totLen = 0
	i = startingIndex + 1 
	fieldsStr = ""
	while buffer[i] != ">":
		fieldsStr += buffer[i]
		i = i + 1 
		totLen = totLen + 1
	fieldsStrss = fieldsStr.split(" ")
	#drop the tag itself
	fieldsStrss.pop(0)
	for field in fieldsStrss:
		keyVal = field.split("=")
		key = keyVal[0]
		#value is optional in html
		if len(keyVal) > 1 :
			val = keyVal[1]
		else:
			val = None 
		atrbs[key] = val
	return atrbs, totLen + 1

#given the openning < of a tag, return all content contained in that tag, excluding the opening and closing tags themselves
#2nd return value is the position of the end of content (last char)
def getTagContent(buf, index):
	rangeHigh = closingTagIndex(buf, index)
	#no closing tag, single tag, no content between tags
	if rangeHigh == -1:
		return ("", index, CLOSING_TAG_NONE)
	#find the lower range start, skip until end of opening 
	rangeLow = index
	while buf[rangeLow] != '>':
		rangeLow = rangeLow + 1
	
	res =  (buf[rangeLow + 1:rangeHigh - 2], rangeHigh - 2, CLOSING_TAG_NORMAL)
	return res


#assuming the root tag opens at index 0 

def printArgsMap(indentDepth, args, outBuf):
	indBlck = ""
	for i in range(0, indentDepth):
			indBlck += tab
	
	for attr, value in args.iteritems():
		#print (indBlck + attr + "=" + value).expandtabs(TAB_WIDTH)
		#outBuf["txt"] += "\n" + (indBlck + attr + "=" + value).expandtabs(TAB_WIDTH)
		outBuf["txt"] += "\n" + (indBlck + attr + "=" + value)
		

#-------------------------------------------TESTS-----------------------------------------
	
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
	printArgsMap(2, args)
	
def testReadArgsLen():
	buf = " <body bgcolor=white>"
	args, len = readTagHeader (buf, 0)
	print len

def testRe():
	#m = re.search('(?<=abc)def', 'abcdef')
	m = re.search('[a-zA-Z0-9_]', '  d  ')
	print m is None
	
#testRe()
	
#testReadArgsLen()	
#parsed = topLevel()
#print "------------------------------------"
#print parsed
#print "done"


