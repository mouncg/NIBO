import threading
import time
import queue

x = False


def consume(q):
    while True:
        name = threading.currentThread().getName()
        print(
            "Thread: {0} start get item from queue[current size = {1}] at time = {2} \n".format(
                name, q.qsize(), time.strftime("%H:%M:%S")
            )
        )
        item = q.get()
        time.sleep(3)  # spend 3 seconds to process or consume the tiem
        print(
            "Thread: {0} finish process item from queue[current size = {1}] at time = {2} \n".format(
                name, q.qsize(), time.strftime("%H:%M:%S")
            )
        )
        q.task_done()


def producer(q):
    global x

    while True:
        # the main thread will put new items to the queue
        if not x:
            pass
        for i in range(10):
            name = threading.currentThread().getName()
            print(
                "Thread: {0} start put item into queue[current size = {1}] at time = {2} \n".format(
                    name, q.qsize(), time.strftime("%H:%M:%S")
                )
            )
            item = "item-" + str(i)
            q.put(item)
            print(
                "Thread: {0} successfully put item into queue[current size = {1}] at time = {2} \n".format(
                    name, q.qsize(), time.strftime("%H:%M:%S")
                )
            )
        q.join()


if __name__ == "__main__":
    x = True
    q = queue.Queue(maxsize=3)

    threads_num = 30  # three threads to consume
    for i in range(threads_num):
        t = threading.Thread(name="ConsumerThread-" + str(i), target=consume, args=(q,))
        t.start()

    # 1 thread to procuce
    t = threading.Thread(name="ProducerThread", target=producer, args=(q,))
    t.start()
    x = False
    if bool(input("RSPT")):
        x = True
    q.join()
