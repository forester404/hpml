!DOCTYPE:
	html
html:
	head:
		meta:
			charset=utf-8
		title:
			leaf:
				HTML5 example with new elements and WAI-ARIA landmark roles
		link:
			media=screen
			href=css/base.css
			type=text/css
			rel=stylesheet
		#:
			[if lte IE 8]>
					<script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
				<![endif]
	body:
		id=index-page
		div:
			id=container
			header:
				role=banner
				h1:
					leaf:
						HTML5 example with new elements and WAI-ARIA landmark roles
				p:
					leaf:
						This page has valid simple HTML5 markup complemented with WAI-ARIA landmark roles for accessibility
			nav:
				id=demo-top-nav
				ul:
					li:
						a:
							href=http://robertnyman.com/html5
							leaf:
								HTML5 demos and samples' start page
					li:
						a:
							href=http://robertnyman.com/
							leaf:
								Robert's talk
					li:
						a:
							href=http://robertnyman.com/javascript/
							leaf:
								JavaScript compatibility tests
			div:
				role=main
				id=demo-main
				section:
					id=demo-main-content
					header:
						hgroup:
							h2:
								leaf:
									A title
							h3:
								leaf:
									Subtitle to the above title
					article:
						p:
							leaf:
								Some content, created
							time:
								datetime=2009-10-14
								leaf:
									October 14th 2009
					article:
						p:
							leaf:
								Some more content - i guess you get the drift by now
					article:
						header:
							h2:
								leaf:
									The HTML code for this page
				aside:
					role=complementary
					id=demo-aside-content
					leaf:
						This is just a demo page to see HTML5 markup and WAI-ARIA landmark roles in action in a simple context
			footer:
				role=contentinfo
				id=page-footer
				leaf:
					Created by
				a:
					href=http://robertnyman.com/
					leaf:
						Robert Nyman