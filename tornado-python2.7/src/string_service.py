import textwrap

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class ReverseHandler(tornado.web.RequestHandler):

	# input is associatted with the regular expression in the handler
	"""
	If there are additional sets of paren-theses in the regular expression, the matched strings will be passed in as additional parameters, in the same order as they occurred in the regular expression.
	"""
	def get(self, input):
		self.write(input[::-1])

class WrapHandler(tornado.web.RequestHandler):
	def post(self):
		text = self.get_argument('text')
		width = self.get_argument('width', 40)
		self.write(textwrap.fill(text, width))


#define multiple methods in the same handler.

# matched with (r"/widget/(\d+)", WidgetHandler)
class WidgetHandler(tornado.web.RequestHandler):

	def get(self, widget_id):
		widget = retrieve_from_db(widget_id)
		self.write(widget.serialize())

	def post(self, widget_id):
		widget = retrieve_from_db(widget_id)
		widget['foo'] = self.get_argument('foo')
		save_to_db(widget)

# matched with (r"/frob/(\d+)", FrobHandler)
class FrobHandler(tornado.web.RequestHandler):
	
	def head(self, frob_id):
		frob = retrieve_from_db(frob_id)

		if frob is not None:
			self.set_status(200)
		else:
			self.set_status(400)

	def get(self, frob_id):
		frob = retrieve_from_db(frob_id)
		self.write(frob.serialize())



if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[
			(r"/reverse/(\w+)", ReverseHandler),
			(r"/wrap", WrapHandler)
		]
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


"""
As with the first example, you can run this program on the command line by typing
the following:

$ python string_service.py --port=8000

The program is a basic framework for an all-purpose web service for string manipula-
tion. Right now, you can do two things with it. First, GET requests to /reverse/string
returns the string specified in the URL path in reverse:

$ curl http://localhost:8000/reverse/stressed
desserts
$ curl http://localhost:8000/reverse/slipup
pupils

$ curl http://localhost:8000/wrap »
-d text=Lorem+ipsum+dolor+sit+amet,+consectetuer+adipiscing+elit.
Lorem ipsum dolor sit amet, consectetuer
adipiscing elit.
"""