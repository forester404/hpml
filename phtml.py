import re

filePath = "sample2.html"


TAG_CLOSING = 1
TAG_OPENNING = 2
TAG_NONE = 3	


tab = "     "
#tab = "\t"
#tab = "tab "


CLOSING_TAG_NONE = 1
CLOSING_TAG_NORMAL = 2
#dbg_file = open("dbg.txt", "w")

def topLevel():
	#dbg_file = open("dbg.txt", "w")

	buffer = readBuffer()
	content, endPos, tagCode = getTagContent(buffer, 0)
	processContent(content, 0)
	
	#dbg_file.close()

def processContent(content, indentInTabs):
	if not content:
		return
	#print "entering processContent(), content = "
	#print content
	i = 0
	while i < len(content):
		strContent = {}
		nextTagPos = nextStargTag(content, i, strContent)
		
		#print simple content in spaces between tags 
		if strContent["txt"]:
			printSimpleContent (indentInTabs, strContent)
		
		
		#if all inner complex elments processed (also true if content was just primitives)
		if nextTagPos == -1:
			return
		#print tag
		tag = readTag(content, nextTagPos)
		indent = ""
		for k in range (0,indentInTabs):
			indent += tab
		print indent + tag + ":"
		
		#print tag args
		args, tagWargsLen = readTagHeader (content, nextTagPos)
		printArgsMap(indentInTabs + 1, args)
		
		#process tag nested content
		tagContent, endTagPos, tagCode = getTagContent(content, nextTagPos)
		if tagCode == CLOSING_TAG_NORMAL:
			processContent(tagContent, indentInTabs + 1)
		
		#else:
			#print "no tag content"
		i = endTagPos 
		
		#if start tag had no matching closing tag, we just #need to consume it. if it had, the pointer would #point at the begining of closing tag, and we need #to consume it
		
		if tagCode == CLOSING_TAG_NONE:
			#i = i + len(tag) + len(">")
			i = i + tagWargsLen + len(">")
			#print "**no closing tag"
		else:
			i = i + len("/>") + len(tag) + len(">")
def readBuffer():
	#buffer = "Read buffer:\n"
	buffer = ""
	buffer += open(filePath, 'rU').read()
	return buffer

def printSimpleContent (indentDepth, simpleConent):
	
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
		print ind + line
		#print "{{{" + ind + line + "}}}"
	#dbg_file.write(ind + line)
	
def nextStargTag(buffer, index, strContent):
	contBuf = ""
	while index < len(buffer):
		if buffer[index] == '<':
			#print "****simple content = " + strContent["txt"] + "***"
			strContent["txt"] = contBuf
			return index
		contBuf += buffer[index]
		index = index + 1
		
	#print "nextStargTag(), reached end of content"
	#strContent["txt"] = ""
	strContent["txt"] = contBuf
	return -1
	
	
#returnn the index to beginning of closing tag, given start index, the index of the opening "<" in openening tag
def closingTagIndex(buffer, startIndex):
	nextTagStart = startIndex
	tagStack = []
	tag = readTag(buffer, startIndex)
	endTag = "</" + tag + ">"
	
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
	#print "entering isTagClosing, index = " + str(index)
	if index < 1:
		raise ValueError("tagType, index must have value > 0")
	if buffer[index - 1] == "/":
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
	#print "***tag = " + tag
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
def getTagContent(buffer, index):
	rangeHigh = closingTagIndex(buffer, index)
	#no closing tag, single tag, no content between tags
	if rangeHigh == -1:
		return ("", index, CLOSING_TAG_NONE)
	#find the lower range start, skip until end of opening 
	rangeLow = index
	while buffer[rangeLow] != '>':
		rangeLow = rangeLow + 1
	
	return (buffer[rangeLow + 1:rangeHigh - 2], rangeHigh - 2, CLOSING_TAG_NORMAL)


	
#print buffer
#print buffer.find("td")


#assuming the root tag opens at index 0 

def printArgsMap(indentDepth, args):
	indBlck = ""
	#indBlck = str(indentDepth)
	for i in range(0, indentDepth):
			indBlck += tab
	#for attr, value in args.__dict__.iteritems():
	for attr, value in args.iteritems():
		#print indBlck + "{}={}".format(attr, value)
		print indBlck + attr + "=" + value
	
def testReadTag():
	buffer = readBuffer()
	print(readTag(buffer, 0))

def testSimpleStringOps():
	tag = "tag"
	print "</" + tag + ">"
	
def testFindFrom():
	#print find("abxxab", 3)
	print "abxxab".find("abrrr", 3)
	
	
def testTagIsClosing():
	print isTagClosing ("<head>", 1)
	print isTagClosing ("</head>", 2)
	print isTagClosing ("head>", 1)
	
	
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
topLevel()


