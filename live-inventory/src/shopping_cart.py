# -*- coding: utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

class ShoppingCart(object):
	""""
	We define a ShoppingCart class that maintains the number of items in our inventory and a list of the shoppers who have added the item to their carts.
	"""
	totalInventory = 10
	callbacks = []
	carts = {}
	
	def register(self, callback):
		self.callbacks.append(callback)
	
	def moveItemToCart(self, session):
		if session in self.carts:
			return
		
		self.carts[session] = True
		self.notifyCallbacks()
	
	def removeItemFromCart(self, session):
		if session not in self.carts:
			return
		
		del(self.carts[session])
		self.notifyCallbacks()
	
	def notifyCallbacks(self):
		self.callbacks[:] = [c for c in self.callbacks if self.callbackHelper(c)]
	
	def callbackHelper(self, callback):
		callback(self.getInventoryCount())
		return False
	
	def getInventoryCount(self):
		return self.totalInventory - len(self.carts)

class DetailHandler(tornado.web.RequestHandler):
	def get(self):
		session = uuid4()
		count = self.application.shoppingCart.getInventoryCount()
		self.render("index.html", session=session, count=count)

class CartHandler(tornado.web.RequestHandler):
	"""
	provides an interface to manipulate the cart
	"""
	def post(self):
		action = self.get_argument('action')
		session = self.get_argument('session')
		
		if not session:
			self.set_status(400)
			return
		
		if action == 'add':
			self.application.shoppingCart.moveItemToCart(session)
		elif action == 'remove':
			self.application.shoppingCart.removeItemFromCart(session)
		else:
			self.set_status(400)

class StatusHandler(tornado.web.RequestHandler):
	"""
	query for notifications of changes to the global inventory.
	"""
	@tornado.web.asynchronous
	def get(self):
		"""
		This instructs Tornado not to close the connection when the get method returns. In the method itself, we simply register a callback with the shopping cart controller. We wrap the callback method with self.async_callback to ensure that exceptions raised in the callback don’t prevent the RequestHandler from properly closing the connection.
		"""
		self.application.shoppingCart.register(self.on_message)
	
	def on_message(self, count):
		"""
		Whenever a visitor’s cart is manipulated, the ShoppingCart controller invokes the on_message method for each of the registered callbacks. This method writes the currentinventory count to the client and closes the connection.
		"""
		self.write('{"inventoryCount":"%d"}' % count)
		self.finish()
		
class Application(tornado.web.Application):
	def __init__(self):
		self.shoppingCart = ShoppingCart()
		
		handlers = [
			(r'/', DetailHandler),
			(r'/cart', CartHandler),
			(r'/cart/status', StatusHandler)
		]
		
		settings = {
			'template_path': 'templates',
			'static_path': 'static'
		}
		
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
	tornado.options.parse_command_line()
	
	app = Application()
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8000)
	tornado.ioloop.IOLoop.instance().start()


