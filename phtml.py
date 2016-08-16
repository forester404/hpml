"""
an interperter from html to cleanView  (python styled synthex)
"""
#TODO - add reference to cleanView reference 


import re
import utils

TAG_CLOSING = 1
TAG_OPENNING = 2
TAG_NONE = 3	
TAB_WIDTH = 5



CLOSING_TAG_NONE = 1
CLOSING_TAG_NORMAL = 2



	
	
def handlePreRoot(buf, outBuf):
	"""
	handles the part above the html tag, that is, the doctype part
	buf -- raw html
	outbuf -- a buffer on which to write the output
	"""
	htmlPos = buf.find("<html", 0)
	contentInfoIndex = buf.find("<!DOCTYPE", 0)
	if contentInfoIndex == -1:
		return htmlPos
	contentStartPos = contentInfoIndex + len("<!DOCTYPE") + 1
	closingPos = buf.find(">", contentStartPos)
	outBuf["txt"] += "\n" + "!DOCTYPE:"
	outBuf["txt"] += "\n" + (utils.TAB + buf[contentStartPos : closingPos])
	return htmlPos





def processContent(content, indentInTabs, outBuf):
	"""
	interprets given raw html sub tree into cleanView subtree
	an html sub tree for that matter is html contined between 2 matching tags
	content - raw html
	indentInTabs - the 
	outBuf - a buffer on which to wirte the interpreted output
	"""
	if not content:
		return
	i = 0
	while i < len(content):
		strContent = {}
		#read content in between tag elements and process it 
		nextTagPos = nextStargTag(content, i, strContent)
		if strContent["txt"]:
			processSimpleContent (indentInTabs, strContent["txt"], outBuf)
		#when all inner complex elments processed (also true if content was just primitives) - processing done
		if nextTagPos == -1:
			return
		#if the current element within content  is a comment 
		if itsAComment(content, nextTagPos):
			commentBlockLen = handleComment(content, indentInTabs, nextTagPos, outBuf)
			i = i + commentBlockLen	
		#else, it's a normal tag 
		else:
			#output tag
			tag = readTag(content, nextTagPos)
			indent = utils.bldInd(indentInTabs)	
			outBuf["txt"] += "\n" + (indent + tag + ":")
			#output tag args
			args, tagWargsLen = readTagHeader (content, nextTagPos)
			outputArgsMap(indentInTabs + 1, args, outBuf)
			#process tag nested content with a recursive invocation 
			tagContent, endTagPos, tagCode = getTagContent(content, nextTagPos)
			if tagCode == CLOSING_TAG_NORMAL:
				processContent(tagContent, indentInTabs + 1, outBuf)
			i = endTagPos 
			
			#if start tag had no matching closing tag, we just #need to consume it. if it had, the pointer would #point at the begining of closing tag, and we need #to consume it
			if tagCode == CLOSING_TAG_NONE:
				i = i + tagWargsLen + len(">")	
			else:
				i = i + len("/>") + len(tag) + len(">")



def handleComment(buf, indentInTabs, startOfOPenTagPos, outBuf):
	"""
	parses and outputs a comment, returns the complet size of the block including tags
	buf - raw html
	indendtInTabs - base indentation depth of subtree
	outBuf -output buffer
	
	how:baiscaly the closing comment tag is searched, and the content is added to output buffer interpreted to cleanView
	"""
	ind = utils.bldInd(indentInTabs)
	pos = startOfOPenTagPos
	output = ""
	startCont = pos + len("<!--")
	endCont = buf.find("-->")
	content = buf[startCont:endCont]
	contentLines = content.split('\n')
	output += "\n" + ind + "#:"
	for line in contentLines:
		output +=  "\n" + ind + utils.TAB + line
	outBuf["txt"] += output
	
	return endCont + len("-->") - startOfOPenTagPos
	
	

def itsAComment(buf, nextTagPos):
	"""
	returns whether given input is an html comment 
	buf - raw html
	nextTagPos - position of suspected tag begining 
	"""
	#for it to be a comment, it must at least the length of openneing and closing tags away from end of buf
	if len(buf) < nextTagPos + 6:
		return False
	#true iff matches open tag
	openTagMatch = buf[nextTagPos + 1 : nextTagPos + 4] == "!--"
	return openTagMatch





def processSimpleContent (indentDepth, rawSimpleContent, outBuf):
	"""
	interpret and output raw html that is leaf, that is not containing tag elements
	indentDepth -- depth of subtree indentation
	rawSimpleContent -- the raw html input 
	outBuf -- buffer to write output on 
	"""
	#if string is only non alphanumeric chars - abort
	m = re.search('[a-zA-Z0-9_]', rawSimpleContent)
	if m is None:
		return
		
	buf = rawSimpleContent
	buf = buf.strip('\t')
	buf = buf.strip('\r')
	ind = utils.bldInd(indentDepth)
	lines = buf.split("\n")
	outBuf["txt"] += "\n" + ind + "leaf:"
	for line in lines:
		if line:
			line = line.strip()
			out = "\n" + ind + utils.TAB + line
			outBuf["txt"] += out
	
	
	
def nextStargTag(buffer, index, strContent):
	"""finds position in given contnet of beginning of next tag"""
	contBuf = ""
	while index < len(buffer):
		if buffer[index] == '<':
			strContent["txt"] = contBuf
			return index
		contBuf += buffer[index]
		index = index + 1
		
	strContent["txt"] = contBuf
	return -1
	
	
def closingTagIndex(buf, startIndex):
	"""
	locates the matching closing tag
	buf -- raw html
	startIndex -- position of openning tag for which closing tag is searched 
	
	returns found position or -1 if not found 
	
	"""
	
	nextTagStart = startIndex
	tagStack = []
	tag = readTag(buf, startIndex)
	
	while nextTagStart < len(buf) and nextTagStart != -1:
		nextTagStart = buf.find(tag, nextTagStart + 1)
		#closing tag - remove the last openneing tag, if the stack is then empty we found we were looking for 
		if nextTagStart == -1:
			return -1
		ttype = tagType(buf, nextTagStart) 
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

	

def tagType(buffer, index):
	"""
	tells weather given html tag is opening  or closing tag
	buffer--raw html
	index--position of the first char in tag name
	""" 
	if index < 1:
		raise ValueError("tagType, index must have value > 0")
	if buffer[index - 2 : index ] == "</":
		return TAG_CLOSING
	if buffer[index - 1] == "<":
		return TAG_OPENNING
	return TAG_NONE
	



def readTag(buffer, startingIndex):
	"""
	extracts the tag name from given raw html tag 
	start index --the index of the opening "<"
	"""
	tag = ""
	i = startingIndex + 1 
	while buffer[i] != ">" and buffer[i] != " ":
		tag += buffer[i]
		i = i + 1
	return tag


def readTagHeader (buffer, startingIndex):
	"""
	parses attributes of given raw html
	buffer -- raw html
	startingIndex -- pointer to beginning of tag
	
	returns a map of attributes and values, and the total length of the raw html tag
	"""
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



def getTagContent(buf, index):
	"""
	extracts content from raw thml - that is, the nested raw html within the tags
	buf -- raw html
	index -- position of openning tag, whose nested content it to be extracted 
	
	returns the extracted nested content 
	"""
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

def outputArgsMap(indentDepth, args, outBuf):
	"""
	translates properties map to cleanView and appends to output
	indentDepth -- indendt depth
	args -- a map of properties and vaues
	outBuf -- buffer to append output to
	
	"""
	indBlck = utils.bldInd(indentDepth)
	for attr, value in args.iteritems():
		outBuf["txt"] += "\n" + (indBlck + attr + "=" + value)
		

#-------------------------------------------TESTS-----------------------------------------
"""	
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
	outputArgsMap(2, args)
	
def testReadArgsLen():
	buf = " <body bgcolor=white>"
	args, len = readTagHeader (buf, 0)
	print len

def testRe():
	#m = re.search('(?<=abc)def', 'abcdef')
	m = re.search('[a-zA-Z0-9_]', '  d  ')
	print m is None
	"""


