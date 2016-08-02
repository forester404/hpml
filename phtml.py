

filePath = "sample2.html"


TAG_CLOSING = 1
TAG_OPENNING = 2
TAG_NONE = 3	


tab = "     "


def topLevel():
	buffer = readBuffer()
	content, endPos = getTagContent(buffer, 0)
	processContent(content, 0)

def processContent(content, indentInTabs):
	if not content:
		return
	#print "entering processContent(), content = "
	#print content
	i = 0
	while i < len(content):
		nextTagPos = nextStargTag(content, i)
		#if all inner complex elments processed (also true if content was just primitives)
		if nextTagPos == -1:
			return
		tag = readTag(content, nextTagPos)
		indent = ""
		for k in range (0,indentInTabs):
			indent += tab
		print indent + tag + ":"
		tagContent, endTagPos = getTagContent(content, nextTagPos)
		processContent(tagContent, indentInTabs + 1)
		
		i = endTagPos 
		#if there is a closing tag
		if tagContent:
			i = i + len(tag) + len(">")
		else:
			i = i + len("/>") + len(tag) + len(">")
def readBuffer():
	#buffer = "Read buffer:\n"
	buffer = ""
	buffer += open(filePath, 'rU').read()
	return buffer

def nextStargTag(buffer, index):
	while index < len(buffer):
		if buffer[index] == '<':
			return index
		index = index + 1
	#print "nextStargTag(), reached end of content"
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
		if isTagClosing(buffer, nextTagStart):
			if len(tagStack) == 1:
				#found it
				return nextTagStart
			else:
					del tagStack[-1]
		#opening tag
		else:
			tagStack.append(tag)
		
	return -1
	#raise ValueError("buffer is not valid html") 
	
#given a location of starting of a tab(1st char), returns true iff the tag is closing one 
#the location is assumed to be in a tag, either openning or closing one 
def isTagClosing(buffer, index):
	#print "entering isTagClosing, index = " + str(index)
	if index < 1:
		return False
	if buffer[index - 1] == "/":
		return True
	if buffer[index - 1] == "<":
		return False
	raise ValueError("input is not first char of openning or closing tag for {}".format(buffer[index - 1:index])) 



#start index is the index of the opening "<"
def readTag(buffer, startingIndex):
	tag = ""
	i = startingIndex + 1 
	while buffer[i] != ">" and buffer[i] != " ":
		tag += buffer[i]
		i = i + 1
	#print "***tag = " + tag
	return tag


#given the openning < of a tag, return all content contained in that tag, excluding the opening and closing tags themselves
#2nd return value is the position of the end of content (last char)
def getTagContent(buffer, index):
	rangeHigh = closingTagIndex(buffer, index)
	#no closing tag, single tag, no content between tags
	if rangeHigh == -1:
		return ("", index)
	#find the lower range start, skip until end of opening 
	rangeLow = index
	while buffer[rangeLow] != '>':
		rangeLow = rangeLow + 1
	
	return (buffer[rangeLow + 1:rangeHigh - 2], rangeHigh - 2)
	
#print buffer
#print buffer.find("td")


#assuming the root tag opens at index 0 
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
		
#testGetContent()	

topLevel()

