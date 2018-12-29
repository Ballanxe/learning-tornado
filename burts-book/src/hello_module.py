import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class HelloHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('hello.html')

class HelloModule(tornado.web.UIModule):
	def render(self):
		return '<h1>Hello, world</h1>'

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[r'/', HelloHandler],
		template_path=os.path.join(os.path.dirname(__file__), 'templates'),
		#Now, when the HelloHandler is invoked and hello.html is rendered, we can use the
		#{% module Hello() %} template tag to include the string returned by the render method
		#in the HelloModule class.
		ui_modules={'Hello', HelloModule}
	)
	server = tornado.httpserver.HTTPServer(app)
	server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


"""
To call this module in templates you use 
<html>
	<head><title>UI Module Example</title></head>
	<body>
		{% module Hello() %}
	</body>
</html>
"""