from parla import Parla, spawn, TaskSpace
from parla import parray as pa

import crosspy as xp
import cupy as cp
import numpy as np

with Parla():
    arr_list = [cp.arange(3), np.arange(2)]
    parr_list = pa.asarray_batch(arr_list)
    a = xp.array(parr_list, axis=0)
    a[0] = a[2] + a[4]
    print(a[0])
