import tornado.ioloop
import tornado.web
import sys
from SimpleQueue import SimpleQueue

queues = {}
path = '/tmp/sqlite.dat'

# concurrent access is fine: will try to run the create if exists statement
def getQueue(queueName):
	if queueName not in queues:
		queue = SimpleQueue(path, queueName)
		queues[queueName] = queue
	else:
	    queue = queues[queueName]
	return queue

def removeQueue(queueName):
	del queues[queueName]

class PeekHandler(tornado.web.RequestHandler):
    def get(self, queueName):
	queue = getQueue(queueName)
	data = queue.peek()
	if data is not None:
	    self.write(data)

class PushHandler(tornado.web.RequestHandler):
    def post(self, queueName):
	queue = getQueue(queueName)
	data = self.request.body
	if data is not None and len(data) > 0:
	    queue.push(data)
	    self.write('OK')
	else:
	    self.write('ERROR')
	
class PopHandler(tornado.web.RequestHandler):
    def get(self, queueName):
	queue = getQueue(queueName)
	data = queue.pop()
	if data is not None:
	    self.write(data)

class SizeHandler(tornado.web.RequestHandler):
    def get(self, queueName):
	queue = getQueue(queueName)
	if queue is None:
	    self.write(0)
	else:
	    self.write(queue.size())

class DropHandler(tornado.web.RequestHandler):
    def drop(self, queueName):
	queue = getQueue(queueName)
	queue.drop()
	removeQueue(queueName)

    def delete(self, queueName):
	self.drop(queueName)
        self.write('OK')

    # in case delete method is not available
    def post(self, queueName):
	self.drop(queueName)
        self.write('OK')

application = tornado.web.Application([
    (r"/queues/([^/]*)/peek", PeekHandler),
    (r"/queues/([^/]*)/size", SizeHandler),
    (r"/queues/([^/]*)/pop", PopHandler),
    (r"/queues/([^/]*)/push", PushHandler),
    (r"/queues/([^/]*)/drop", DropHandler)
])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('Usage: HttpQueue.py <SQLite file> <port>')
	
    path = sys.argv[1]
    port = int(sys.argv[2])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
