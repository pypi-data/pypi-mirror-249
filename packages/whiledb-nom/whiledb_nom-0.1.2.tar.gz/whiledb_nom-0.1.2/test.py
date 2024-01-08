import whiledb_nom
from concurrent.futures import ThreadPoolExecutor
import time


start = time.time()

executor = ThreadPoolExecutor()
map(lambda x: x.result(), [
    executor.submit(
        whiledb_nom.exec,
        """
        i = 0;
        while i < 300 {
            acc = 0; idx = 0;
            while idx < 10000 {
                acc = acc + idx ^ 3;
                idx = idx + 1; 
            }
            i = i + 1;
        }
        """
    ) for _ in range(10)
])
print(time.time() - start)


start = time.time()

i = 0
while i < 3000:
    acc, idx = 0, 0
    while idx < 10000:
        acc = acc + idx ** 3
        idx = idx + 1
    i = i + 1

print(time.time() - start)
