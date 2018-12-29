# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

"""
any option in a define() statement will become available as an attribute of the global options object, if an option with the same name is given on the command line. If the user runs the program with the help parameter, the program will print out all of the options you’ve defined, along with the text you specified with the help parameter in the call to define . If the user fails to provide a value for an option we specified, the default value for that option will be used instead.
#Our line, therefore, allows the user to use an integer port argument, which we can access in the body of the program as options.port . If the user doesn’t specify a value, it defaults to 8000 .

"""
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	"""
	In this example, we’ve defined only a get method, meaning that this handler will respond only to HTTP GET requests.

	"""
	def get(self):
		# This variable can be accessed in the http curl request.
		# First argument is the name of the variable on the url , second is the default value
		greeting = self.get_argument('greeting', 'Hello')
		self.write(greeting + ', friendly user!')

		"""
		If you’d like to replace the default error responses with your own, you can override the write_error method in your RequestHandler class.
		"""
	def write_error(self, status_code, **kwargs):

		self.write("Gosh darnit, user! You caused a %d error." % status_code)

if __name__ == "__main__":
	#we use Tornado’s options library to parse the command line.
	tornado.options.parse_command_line()
	"""
	The most important argument to pass to the __init__
	method of the Application class is handlers . This tells Tornado which classes to use to
	handle which requests.
	"""
	"""
	should be a list of tuples, with each tuple containing a regular expression to match as its first member and a RequestHandler class as its second member.

	"""
	app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


"""
Most of the work in making a Tornado application is to define classes that extend the
Tornado RequestHandler class. In this case, we’ve made a simple application that listens
for requests on a given port, and responds to requests to the root resource ( "/" ).
Try running the program yourself on the command line to test it out:

$ python hello.py --port=8000

Now you can go to http://localhost:8000/ in a web browser, or open up a separate
terminal window to test out the application with curl:

$ curl http://localhost:8000/
Hello, friendly user!
$ curl http://localhost:8000

"""