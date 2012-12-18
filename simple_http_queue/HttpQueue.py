import tornado.ioloop
import tornado.web
import sys
from SimpleQueue import SimpleQueue

queues = {}
stacks = {}
path = '/tmp/sqlite.dat'

# concurrent access is fine: will try to run the create if exists statement
def getQueue(queueName):
	if queueName not in queues:
		queue = SimpleQueue(path, queueName, SimpleQueue.FIFO)
		queues[queueName] = queue
	else:
	    queue = queues[queueName]
	return queue

def getStack(stackName):
	if stackName not in stacks:
		stack = SimpleQueue(path, stackName, SimpleQueue.LIFO)
		stacks[stackName] = stack
	else:
	    stack = stacks[stackName]
	return stack

def removeQueue(queueName):
	del queues[queueName]

def removeStack(stackName):
	del stacks[stackName]

class QueuePeekHandler(tornado.web.RequestHandler):
    def get(self, queueName):
	queue = getQueue(queueName)
	data = queue.peek()
	if data is not None:
	    self.write(data)

class QueuePushHandler(tornado.web.RequestHandler):
    def post(self, queueName):
	queue = getQueue(queueName)
	data = self.request.body
	if data is not None and len(data) > 0:
	    queue.push(data)
	    self.write('OK')
	else:
	    self.write('ERROR')
	
class QueuePopHandler(tornado.web.RequestHandler):
    def get(self, queueName):
	queue = getQueue(queueName)
	data = queue.pop()
	if data is not None:
	    self.write(data)

class QueueSizeHandler(tornado.web.RequestHandler):
    def get(self, queueName):
	queue = getQueue(queueName)
	if queue is None:
	    self.write(0)
	else:
	    self.write(queue.size())

class QueueDropHandler(tornado.web.RequestHandler):
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

class StackPeekHandler(tornado.web.RequestHandler):
    def get(self, stackName):
	stack = getStack(stackName)
	data = stack.peek()
	if data is not None:
	    self.write(data)

class StackPushHandler(tornado.web.RequestHandler):
    def post(self, stackName):
	stack = getStack(stackName)
	data = self.request.body
	if data is not None and len(data) > 0:
	    stack.push(data)
	    self.write('OK')
	else:
	    self.write('ERROR')
	
class StackPopHandler(tornado.web.RequestHandler):
    def get(self, stackName):
	stack = getStack(stackName)
	data = stack.pop()
	if data is not None:
	    self.write(data)

class StackSizeHandler(tornado.web.RequestHandler):
    def get(self, stackName):
	stack = getStack(stackName)
	if stack is None:
	    self.write(0)
	else:
	    self.write(stack.size())

class StackDropHandler(tornado.web.RequestHandler):
    def drop(self, stackName):
	stack = getStack(stackName)
	stack.drop()
	removeStack(stackName)

    def delete(self, stackName):
	self.drop(stackName)
        self.write('OK')

    # in case delete method is not available
    def post(self, stackName):
	self.drop(stackName)
        self.write('OK')

application = tornado.web.Application([
    (r"/queues/([^/]*)/peek", QueuePeekHandler),
    (r"/queues/([^/]*)/size", QueueSizeHandler),
    (r"/queues/([^/]*)/pop", QueuePopHandler),
    (r"/queues/([^/]*)/push", QueuePushHandler),
    (r"/queues/([^/]*)/drop", QueueDropHandler),
    (r"/stacks/([^/]*)/peek", StackPeekHandler),
    (r"/stacks/([^/]*)/size", StackSizeHandler),
    (r"/stacks/([^/]*)/pop", StackPopHandler),
    (r"/stacks/([^/]*)/push", StackPushHandler),
    (r"/stacks/([^/]*)/drop", StackDropHandler)

])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('Usage: HttpQueue.py <SQLite file> <port>')
	
    path = sys.argv[1]
    port = int(sys.argv[2])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
