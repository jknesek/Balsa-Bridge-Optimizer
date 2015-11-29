import pyprind
import time
import sys


n = 100
bar = pyprind.ProgBar(n, bar_char='█')
for i in range(n):
    time.sleep(0.1) # do some computation
    bar.update()