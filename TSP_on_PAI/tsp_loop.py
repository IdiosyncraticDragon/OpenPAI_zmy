#from pyspark.context import SparkContext
from pyspark.sql import SparkSession
import numpy as np
import time,os,sys
#-------------initiation-------------#
# sc=SparkContext()


max_time=30*60
max_iter=10000
threshold=10.0
work_path='/shared/TSP/'
print("waiting for the matrix.")


#------------initiation over---------#

#print("GOOD")
if __name__=="__main__":
    spark=SparkSession\
        .builder\
        .appName("Demo2")\
        .getOrCreate()
    

    import create as tc
    import os_file as to
    import iteration as it

    from pai_pyhdfs import wait_hdfs_file,hdfs_save

    f=wait_hdfs_file(work_path,'distance_matrix.npy',delete=False)
    m=np.load(f,allow_pickle=True) #save distance_matrix in m.

    def get_res(s1,s2):
        if tc.cost(s1,m)<tc.cost(s2,m):
            return s1
        else:
            return s2

    while True:
        f=wait_hdfs_file(work_path,'generations.npy',delete=False)
        generations=np.load(f)
        print("generation information getted. Now setting the gen_rdd.")
        gen_rdd=spark.sparkContext.parallelize(generations)
        print("rdd setted,now maping.")
        res=gen_rdd.map(lambda x:it.iteration(x,m))
        print("mapping over,now reducing.")
        res2=res.reduce(get_res)
        print("The best solution is:",res2)
        c=tc.cost(res2,m)
        print("The lowest cost is :",c)
        hdfs_save(work_path,'final_solution.npy',[res2,c])

