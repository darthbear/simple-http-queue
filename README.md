simple-http-queue
=================

Very simple HTTP queue implemented using Python, SQLite3 and Tornado

Run the server:
python HttpQueue.py /tmp/myqueue.dat 8080

How to use it:
push: curl http://localhost:8080/<queue>/push -XPOST -d 'my_data'
pop: curl http://localhost:8080/<queue>/pop
peek: curl http://localhost:8080/<queue>/peek
size: curl http://localhost:8080/<queue>/size
drop: curl http://localhost:8080/<queue>/drop -XDELETE
