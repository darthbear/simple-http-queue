simple-http-queue
=================

Very simple HTTP queue implemented using Python, SQLite3 and Tornado

Run the server:
python HttpQueue.py /tmp/myqueue.dat 8080

How to use it:
push: curl http://localhost:8080/myqueue1/push -XPOST -d 'mydata'
pop: curl http://localhost:8080/myqueue1/pop
peek: curl http://localhost:8080/myqueue1/peek
size: curl http://localhost:8080/myqueue1/size
drop: curl http://localhost:8080/myqueue1/drop -XDELETE

You can use as many queues as you want
