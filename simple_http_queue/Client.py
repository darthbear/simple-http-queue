import urllib
import urllib2

class Client(object):
    url_pattern = 'http://%s:%d/queues/%s/%s'

    def __init__(self, hostname, port, name):
	self.hostname = hostname
	self.port = port
	self.name = name

    def peek(self):
	req = urllib2.Request(self.url_pattern%(self.hostname, self.port, self.name, 'peek'))
	response = urllib2.urlopen(req)
	return response.read()

    def pop(self):
	req = urllib2.Request(self.url_pattern%(self.hostname, self.port, self.name, 'pop'))
	response = urllib2.urlopen(req)
	return response.read()

    def size(self):
	req = urllib2.Request(self.url_pattern%(self.hostname, self.port, self.name, 'size'))
	response = urllib2.urlopen(req)
	return int(response.read())

    def push(self, data):
	req = urllib2.Request(self.url_pattern%(self.hostname, self.port, self.name, 'push'), data)
	response = urllib2.urlopen(req)
	return response.read()

    def drop(self):
	req = urllib2.Request(self.url_pattern%(self.hostname, self.port, self.name, 'drop'), '')
	response = urllib2.urlopen(req)
	return response.read()


def test(hostname, port, queue):
    c = Client(hostname, port, queue)
    print c.push('data1')
    print c.push('data2')
    print c.push('data3')
    print c.peek()
    print c.size()
    print c.pop()
    print c.pop()
    print c.pop()
    print c.drop()

#test('localhost', 8888, 'queue1')
