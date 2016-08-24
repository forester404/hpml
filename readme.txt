page19	overview 
----------------					
Page19 is an alternative representation of html, its style is inspired by Python indentation-sensitive and clean syntax.
Motivation being finding normal html syntax really ugly and verbose. 

so instead of:

<tag1 prop1="val1" prop2="val2">
	<!--comment text-->
	<nestedTag prop11="val11" prop12="val12">plain string</nestedTag>
</tag1>

you get:

tag1:
	prop1 = val1
	prop2 = val2
	#:
		comment text
	nestedTag:
		prop11 = val11
		prop12 = val12
		leaf:
			plain string

to see more extensive examples:
you can view the .pig files in /testing/test_input. you can also uncomment and run /testing/tester.demoConsoleBackAndForthHTML() 
for an instance of the translated syntax of a test file to be printed to console. 
the functionality supported by the project is translating in both directions html->page19 and the other way around.
in general the project is only a demo and not an actual product. it has no pretence to fully support the HTML specification, 
but enough of the basic stuff to be a useful demo, i hope. 
although originally designed to work with html, it has occured to me that it probably could work with slight modification 
more generally with any xml, but like everything in life it turned out to be more complicated than expected, so the support 
for general XML is very limited at the moment. 

the API (see comments in code for more details)
-----------------------------------------------
the phtml module translates from html to page19, with translateRawHtml()  
it also translates xml to page with the translateXML()  

the goBack module translates from page19 to html with translageBacktoHtml(), and 
page19 to xml with processBuf()

in the tester module you can either run the tests, or the demos by uncommenting proper function call at the bottom of the file

usage
-----
created with python 2.7
to run the tester in windows command line just unpack project, change your location to the testing folder and enter:
python tester.py 
(assuming you have python installed and included in your path. otherwise consult python documantation)
on others platforms i imagine it is something very similar 
otherwise, just use the api as normal python modules 




status
-------
22.08.2016 
the basic functionality of translating between html and page19 is implemented and superficially tested. 
the functionality includes almost no error handling.
the testing is comprised mostly of high level functionality, testing of low lever helping function is missing.  
translating of general xml functions only with basic stuff like xml_simple_1 but fails on more complex 
stuff like soap1.xml and soap2.xml


contact
--------
please contact me at odedwolff@gmail.com or via github for any kind of feedback or questions

 

