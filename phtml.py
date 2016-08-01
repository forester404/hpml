

filePath = "sample2.html"



def readBuffer():
	#buffer = "Read buffer:\n"
	buffer = ""
	buffer += open(filePath, 'rU').read()
	return buffer

#start index is the index of the opening "<" in openening tag
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
		#openning tag
		else:
			tagStack.append(tag)
		
	raise ValueError("buffer is not valid html") 
	
#given a location of starting of a tab(1st char), returns true iff the tag is closing one 
#the location is assumed to be in a tag, either openning or closing one 
def isTagClosing(buffer, index):
	print "entering isTagClosing, index = " + str(index)
	if index < 1:
		return False
	if buffer[index - 1] == "/":
		return True
	if buffer[index - 1] == "<":
		return False
	raise ValueError("input is not first char of openning or closing tag") 
	

#start index is the index of the opening "<"
def readTag(buffer, startingIndex):
	tag = ""
	i = startingIndex + 1 
	while buffer[i] != ">":
		tag += buffer[i]
		i = i + 1
	print "***tag = " + tag
	return tag
	
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
		
testFindEndOfRoot()	
