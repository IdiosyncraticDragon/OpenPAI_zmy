import create as tc
import os_file as to
import iteration as it
import numpy as np
import time,os,sys
from pai_pyhdfs import *
#from pyspark.context import SparkContext
from pyspark.sql import SparkSession

#-------------initiation-------------#
# sc=SparkContext()



# max_time=30*60
# max_iter=10000
# threshold=10.0
# work_path='/shared/TSP/'
# print("waiting for the matrix.")
# f=wait_hdfs_file(work_path,'distance_matrix.npy',delete=False)
# m=np.load(f,allow_pickle=True) #save distance_matrix in m.

# def get_res(s1,s2):
#     if tc.cost(s1,m)<tc.cost(s2,m):
#         return s1
#     else:
#         return s2

# #------------initiation over---------#

# #print("GOOD")
# while True:
#     f=wait_hdfs_file(work_path,'generations.npy',delete=False)
#     generations=np.load(f)
#     print("generation information getted. Now setting the gen_rdd.")
#     gen_rdd=spark.sparkContext.parallelize(generations)
#     print("rdd setted,now maping.")
#     res=gen_rdd.map(lambda x:it.iteration(x,m))
#     print("mapping over,now reducing.")
#     res2=res.reduce(get_res)
#     print("The best solution is:",res2)
#     c=tc.cost(res2,m)
#     print("The lowest cost is :",c)
#     hdfs_save(work_path,'final_solution.npy',[res2,c])

from random import random
from operator import add

if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    spark=SparkSession\
    .builder\
        .appName("Demo2")\
            .getOrCreate()
            
    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n = 100000 * partitions

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    print("Pi is roughly %f" % (4.0 * count / n))

    spark.stop()