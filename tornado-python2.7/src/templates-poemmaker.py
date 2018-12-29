import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

class PoemPageHandler(tornado.web.RequestHandler):
	def post(self):

		noun1 = self.get_argument('noun1')
		noun2 = self.get_argument('noun2')
		verb = self.get_argument('verb')
		noun3 = self.get_argument('noun3')
		"""
		Once we’ve told Tornado where to find templates, we can use the render method of the RequestHandler class to tell Tornado to read in a template file, interpolate any template code found within, and then send the results to the browser. The variables are template placeholders
		"""
		self.render('poem.html', roads=noun1, wood=noun2, made=verb, difference=noun3)


if __name__ == '__main__':

	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r'/', IndexHandler), (r'/poem', PoemPageHandler)],
		template_path=os.path.join(os.path.dirname(__file__), "templates")
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


# python templates-poemmaker.py --port=8000
"""
You can try out the templating system outside of a Tornado application by importing the template module in the Python interpreter, and printing the output directly.
"""
"""
>>> from tornado.template import Template
>>> content = Template("<html><body><h1>{{ header }}</h1></body></html>")
>>> print content.generate(header="Welcome!")
<html><body><h1>Welcome!</h1></body></html>
"""

"""
It turns out that you can put any Python expression inside double curly braces. Tornado will insert a string containing whatever that expression evaluated to into the output. Here are a few examples of what’s possible:
"""

"""
>>> from tornado.template import Template
>>> print Template("{{ 1+1 }}").generate()
2
>>> print Template("{{ 'scrambled eggs'[-4:] }}").generate()
eggs
>>> print Template("{{ ', '.join([str(x*x) for x in range(10)])}}").generate()
0, 1, 4, 9, 16, 25, 36, 49, 64, 81
"""

"""
You can also include Python conditionals and loops in your Tornado templates. Con-
trol statements are surrounded by {% and %} , and are used in cases like:
{% if page is None %}
or
{% if len(entries) == 3 %}

"""

# class BookHandler(tornado.web.RequestHandler):
# 	def get(self):
# 		self.render(
# 			"book.html",
# 			title="Home Page",
# 			header = "Books that are great",
# 			books=[
# 				"Learning Python",
# 				"Programming Collective Intelligence",
# 				"Restful Web Services"
# 			]
# 			)

"""
<html>
	<head>
		<title>{{ title }}</title>
	</head>
	<body>
		<h1>{{ header }}</h1>
		<ul>
		{% for book in books %}
		<li>{{ book }}</li>
		{% end %}
		</ul>
	</body>
</html>

"""

"""
Using Functions Inside Templates Tornado offers several handy functions by default in all templates. These include:

escape(s) = Replaces & , < , and > in string s with their corresponding HTML entities.

url_escape(s) = Uses urllib.quote_plus to replace characters in string s with URL-encoded equivalents.

json_encode(val) = Encodes val as JSON. (Underneath the hood, this is just a call to the dumps function in the json library. See the relevant documentation for information about what parameters this function accepts and what it returns.)

squeeze(s) = Filters string s, replacing sequences of more than one whitespace character with a single space.

"""

#The generate function allows to execute python functions insider template placeholders
"""
>>> from tornado.template import Template
>>> def disemvowel(s):
...
return ''.join([x for x in s if x not in 'aeiou'])
...
>>> disemvowel("george")
'grg'
>>> print Template("my name is {{d('mortimer')}}").generate(d=disemvowel)
my name is mrtmr
"""