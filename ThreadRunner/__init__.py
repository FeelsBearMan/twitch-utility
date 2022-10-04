import os
import threading
import time


class ThreadRunner:
    def __init__(self) -> None:
        super().__init__()
        self.THREAD_COUNTS = os.cpu_count()

    def run(self, execution_function, task_list, *args):
        threads = []

        task_size = len(task_list)

        d = task_size // self.THREAD_COUNTS
        r = task_size % self.THREAD_COUNTS

        # Measure the elapsed time between two points
        start = time.perf_counter()

        for i in range(self.THREAD_COUNTS):
            task_start = i * d + r
            task_end = (i + 1) * d + r
            if i < r:
                task_start = i * d + i % self.THREAD_COUNTS
                task_end = (i + 1) * d + i % self.THREAD_COUNTS + 1
            if task_start == task_end:
                break

            t = threading.Thread(target=execution_function,
                                 args=(task_list[task_start:task_end], *args))
            t.start()
            threads.append(t)

        # Join all threads
        for thread in threads:
            thread.join()

        end = time.perf_counter()

        return end - start
