import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

from tornado.options import define, options
define("ports", default=8000, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		cookie = self.get_secure_cookie("count")
		count = int(cookie) + 1 if cookie else 1

		countString = "1 time" if count == 1 else "%d times" % count

		self.set_secure_cookie("count", str(count))

		self.write(
			'<html><head><title>Cookie Counter</title></head>'
			'<body><h1>You&rsquo;ve viewed this page %s times.</h1>' % countString
			'</body></html>'
		)

if __name__ == "__main__":
	tornado.options.parse_command_line()

	settings = {
		"cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E="
	}

	application = tornado.web.Application([
		(r'/', MainHandler)
	], **settings)

	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

"""
The cookie_secret value passed to the Application constructor should
be a unique, random string. Executing the following code snippet in a
Python shell will generate one for you:

>>> import base64, uuid
>>> base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E='

-----------

Making a cookie available just with ssl connections and inaccessible to Javascript:

self.set_cookie("'foo', 'bar', httponly=True, secure=True")

----------

You can enable XSRF protection by including the xsrf_cookies parameter in the application’s constructor:

	settings = {
	"cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
	"xsrf_cookies": True
	}

Tornado will handle the xsrf cookies behind the scenes, but you must include the XSRF token in your HTML forms in order to authorize legitimate requests.

<form action="/purchase" method="POST">
	{% raw xsrf_form_html() %}
	<input type="text" name="title" />
	<input type="text" name="quantity" />
	<input type="submit" value="Check Out" />
</form>

--------------

AJAX requests also require an _xsrf parameter, but instead of having to explicitly in-
clude an _xsrf value when rendering the page, the script is able to query the browser
for the value of the cookie on the client side. The following two functions transparently
add the token value to AJAX POST requests.


function getCookie(name) {
var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
return c ? c[1] : undefined;

jQuery.postJSON = function(url, data, callback) {
	data._xsrf = getCookie("_xsrf");
	jQuery.ajax({
		url: url,
		data: jQuery.param(data),
		dataType: "json",
		type: "POST",
		success: callback
	});
}


"""
