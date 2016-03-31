# -*- coding:utf8 -*-
#!/usr/bin/python
 
import socket
import threading
import Queue
import sys
class worker(threading.Thread):
    def __init__(self, name, queue, port1, port2):
        super(worker,self).__init__(name = name)
        self.data = queue
        self.port1 = port1
        self.port2 = port2
    def run(self):
        for i in range(self.port1, self.port2):
            self.data.put(i)
 
class customer(threading.Thread):
    def __init__(self, name, queue):
    	self.data = queue
        super(customer, self).__init__(name = name)
    def scan(self, ip, port):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        results = s.connect_ex((ip, port))
        if (results==0):
            print 'Port %d: OPEN' % port
        s.close()
 
    def run(self):
        while True:
            try:
                a = self.data.get(1, 5)
            except:
                break
            else:
                ip = sys.argv[1]
                self.scan(ip, a)
def main():
    queue = Queue.Queue()
    pool = []
    port1 = int(sys.argv[2])
    port2 = int(sys.argv[3])
    workers = worker('queengina', queue, port1, port2)
    workers.start()
    for i in range(100):
        customers = customer('queengina', queue)
        pool.append(customers)
    for i in pool:
        i.start()
    workers.join()
    for i in pool:
        i.join()
    del pool[:]
if __name__=='__main__':
    main()
