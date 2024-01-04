# api test


This test is about REST API and AMQP.

The control version that I am using is git, so you can find two branches:  

* master: It is a simple use of REST API. To do this, I am using flask, and to register the visits I am using a defined logger
* AMQP: It is the same that the previous one, but using a declared queue to register the visits.

The possible path are:

* http://localhost:5000/
* http://localhost:5000/path_1
* http://localhost:5000/path_2
* http://localhost:5000/path_1/sub_path_1
* http://localhost:5000/unique_visited
* http://localhost:5000/history
* http://localhost:5000/close_amqp

There are two endpoints more. It's just for see on the web browser
* http://localhost:5000/path_1/unique_visited_readable
* http://localhost:5000/path_1/history_readable


# Using the script

The main script is 'app.py' to run it, you must type the following:

```
python app.py
```

If you desire mount the server in another ip you should type the following:

For instance, at the ip 192.168.1.128
```
python app.py 192.168.1.128
```

To stop the server, you must follow this steps:

1. Go to http://localhost:5000/close_amqp. That will execute a close_consuming function to the queue. This step is done on the AMQP branch, not otherwise. 
2. Then, you can stop the server using the shortcut CTRL+C