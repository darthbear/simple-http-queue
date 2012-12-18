simple-http-queue
=================

Very simple HTTP queue implemented using Python, SQLite3 and Tornado

Run the server:

	python HttpQueue.py /tmp/data.dat 8080

How to use queues:

	push: curl http://localhost:8080/queues/myqueue1/push -XPOST -d 'mydata'
	pop: curl http://localhost:8080/queues/myqueue1/pop
	peek: curl http://localhost:8080/queues/myqueue1/peek
	size: curl http://localhost:8080/queues/myqueue1/size
	drop: curl http://localhost:8080/queues/myqueue1/drop -XDELETE
	drop: curl http://localhost:8080/queues/myqueue1/drop -XPOST

How to use stacks:

	push: curl http://localhost:8080/stacks/mystack1/push -XPOST -d 'mydata'
	pop: curl http://localhost:8080/stacks/mystack1/pop
	peek: curl http://localhost:8080/stacks/mystack1/peek
	size: curl http://localhost:8080/stacks/mystack1/size
	drop: curl http://localhost:8080/stacks/mystack1/drop -XDELETE
	drop: curl http://localhost:8080/stacks/mystack1/drop -XPOST

You can use as many queues as you want

Client:

	Client.py offers a thin interface to the queue/stack
