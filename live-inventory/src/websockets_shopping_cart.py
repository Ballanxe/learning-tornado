# -*- coding: utf-8 -*-
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

class ShoppingCart(object):
	"""
	We define a ShoppingCart class that maintains the number of items in our inventory and a list of the shoppers who have added the item to their carts.
	"""
	totalInventory = 10
	callbacks = []
	carts = {}
	
	def register(self, callback):
		self.callbacks.append(callback)

	def unregister(self, callback):
		self.callbacks.remove(callback)
	
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
		for callback in self.callbacks:
			callback(self.getInventoryCount)
	
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

class StatusHandler(tornado.websocket.WebSocketHandler):
	"""
	query for notifications of changes to the global inventory.
	"""
	def open(self):
		self.application.shoppingCart.register(self.callback)

	def on_close(self):
		self.application.shoopingCart.unregister(self.callback)

	def on_message(self, message):
		"""
		Since we’re still using the HTTP API calls in the CartHandler class, we don’t listen for new messages on the WebSocket connection, so the on_message implementation is empty. (We override the default implementation of on_message to prevent Tornado from raising a NotImplementedError if we happen to receive a message.)
		"""
		pass

	def callback(self, count):
		self.write_message("{'inventoryCount':'%d'}" % count)

		
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













