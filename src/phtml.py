"""
an translator from html to page19  (python styled synthex)
"""

#TODO - implement error handling 

import re
import utils



TAG_CLOSING = 1
TAG_OPENNING = 2
TAG_NONE = 3	
TAB_WIDTH = 5



CLOSING_TAG_NONE = 1
CLOSING_TAG_NORMAL = 2


def translateRawHtml(rawHtml):
	"""
	translates a buffer of raw html to page19 syntax
	"""
	outBuf = {}
	outBuf["txt"] = ""
	buf = rawHtml
	rootStart = handlePreRoot(buf, outBuf)
	content, endPos, tagCode = getTagContent(buf, rootStart)
	outBuf["txt"] += "\n" + "html:"
	processContent(content, 1, outBuf)
	return outBuf["txt"]




def translateXML(rawXml):
	"""
	translates xml to page19
	this is only a partial implementation, that is, it would fail on some xml 
	"""
	#TODO - complete/fix implementation 
	
	outBuf = {}
	outBuf["txt"] = ""
	buf = rawXml
	processContent(buf, 1, outBuf)
	return outBuf["txt"]

	
	
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
	translates given raw html sub tree into page19 subtree
	an html sub tree for that matter is html contined between 2 matching tags
	content - raw html
	indentInTabs - the 
	outBuf - a buffer on which to write the interpreted output
	
	the function itterates over subblocks of the current level- siblings in the html sub tree 
	each sibling is either a nested tag and its optional a comment, or a primitive content, that is, a simple string
	"""
	if not content:
		return
	i = 0
	while i < len(content):
		strContent = {}
		#read content in between tag elements and processes it (between ending of one tag and begining of its sibling)
		nextTagPos = nextStargTag(content, i, strContent)
		if strContent["txt"]:
			processSimpleContent (indentInTabs, strContent["txt"], outBuf)
		#when all inner complex elments processed (also true if content was just primitives) - processing done
		#the processing of the primitive contnet is done while looking for the next tab, see above
		if nextTagPos == -1:
			return
		#if the current element within content  is a comment 
		if itsAComment(content, nextTagPos):
			commentBlockLen = handleComment(content, indentInTabs, nextTagPos, outBuf)
			i = i + commentBlockLen	
		#else, it's a normal nested tag
		else:
			#output tag
			tag = readTag(content, nextTagPos)
			indent = utils.bldInd(indentInTabs)	
			outBuf["txt"] += "\n" + (indent + tag + ":")
			#output tag properties
			args, tagWargsLen = readTagHeader (content, nextTagPos)
			outputArgsMap(indentInTabs + 1, args, outBuf)
			#process tag nested content with a recursive invocation 
			tagContent, endTagPos, tagCode = getTagContent(content, nextTagPos)
			if tagCode == CLOSING_TAG_NORMAL:
				processContent(tagContent, indentInTabs + 1, outBuf)
			i = endTagPos 
			
			#if start tag had no matching closing tag, we just need to consume it. if it had, the pointer would #point at the begining of closing tag, and we need #to consume it
			if tagCode == CLOSING_TAG_NONE:
				i = i + tagWargsLen + len(">")	
			else:
				i = i + len("/>") + len(tag) + len(">")



def handleComment(buf, indentInTabs, startOfOPenTagPos, outBuf):
	"""
	translates a comment and appends to output buffer, returns the complete size of the block including tags
	buf - raw html
	indendtInTabs - base indentation depth of subtree
	outBuf -output buffer
	
	how:baiscaly the closing comment tag is searched, and the content is added to output buffer interpreted to page19
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
	translates and outputs raw html that is leaf, that is not containing tag elements
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
	"""finds position in given content of beginning of next tag"""
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



def readTagHeader(buf, pos):
	"""
	parses raw html to a map of properties and values, 
	return parsed properties and buffer length consumed
	"""
	i = pos + 1 
	props = {}
	propNum = 0
	while i < len(buf) and buf[i] != ">":
		key, consumed = readPropKey(buf, i)
		i = i + consumed 
		if not key:
			continue
		val, consumed = readPropVal(buf, i)
		i = i + consumed 
		if propNum > 0:
			props[key] = val 
		propNum = propNum + 1
		
	totLen = i - pos + 1 
	return props, totLen

#returns the property and length		
def readPropKey(buf, pos):
	"""
	parses property name from raw html, returns propery name and buffer length consumed
	"""
	i = pos
	out = ""
	#skip open char and spaces
	while i < len(buf) and buf[i] == " " and not buf[i] == ">":
		i = i + 1
	#no further key 
	if buf[i] == ">":
		return None, i - pos
	#now read actual word - it ends either with assignment or whitespace 	
	while buf[i] != " " and buf[i] != "=" and not buf[i] == ">" and i < len(buf):
		out += buf[i]
		i = i + 1
	return out, i - pos 


def readPropVal(buf, pos):
	"""
	parses raw html to property value. returns value and consumed buffer length.  
	pos is assumed to  point at anywhere between next char after the correspinding 
	(preceeding)key and the "=" if there is one. a "=" exists iff a value exists. 
	otherwise None is returned. 
	returns value (if exists) and length consumed, if  value doesnt exist consumed value 
	is 0, because the same position should be called with again, searching for the next property 
	name (for instance <tagNamee perop1="Val1" prop2 prope3="val3">)
	prop2 has no value, so we will first try to read past prop2, but than find out it has no value, so
	we will have to try reading it again as a property (not value) this time. see readPropKey()
	
	"""
	
	
	i = pos
	#consume whitespaces
	while i < len(buf) and buf[i] == " " and not buf[i] == ">":
		i = i + 1
	#no assignment, hit the next prop key 	
	if buf[i] != "=":
		#return None, i -  pos
		return None, 0
	#cosume white spaces pass assignment
	i = i + 1
	while buf[i] == " ":
		i = i + 1
	#prop value may be either be or not be within qoutues 
	val = ""
	#no quoutes 
	if buf[i] != '"' and  buf[i] != "'" :
		while buf[i] != " " and buf[i] != ">":
			val += buf[i]
			i = i + 1 
			
		return val, i - pos
	#with quotes
	quoteChar = buf[i]
	i = i + 1
	while  buf[i]!= quoteChar:
		val += buf[i]
		i = i + 1
		
	return val, i - pos + 1
	

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




def outputArgsMap(indentDepth, args, outBuf):
	"""
	translates properties map to page19 and appends to output
	indentDepth -- indendt depth
	args -- a map of properties and vaues
	outBuf -- buffer to append output to
	
	"""
	indBlck = utils.bldInd(indentDepth)
	for attr, value in args.iteritems():
		if not value:
			valStr = ""
		else:
			valStr = str(value)
		#outBuf["txt"] += "\n" + (indBlck + attr + "=" + value)
		outBuf["txt"] += "\n" + (indBlck + attr + "=" + valStr)
		




