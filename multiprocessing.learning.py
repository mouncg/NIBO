import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from os import system as s
from time import sleep as sl
import time
from concurrent import futures

start = time.perf_counter()


def run():

    sl(10)
    return "yeet"


# if __name__ == "__main__":
#     lx = []
#     for _ in range(10):
#         p = multiprocessing.Process(target=run)
#         p.start()
#         lx.append(p)
#     for _ in lx:
#         _.join()
#     end = time.perf_counter()
#     print(f"finished in {round(end - start, 2)} seconds.")
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        # t = executor.submit(run)
        #
        # t.result()
        rst = [executor.submit(run) for _ in range(15)]
        for f in futures.as_completed(rst):
            print(f.result())
        end = time.perf_counter()
        print(f"finished in {round(end - start, 2)} seconds.")
