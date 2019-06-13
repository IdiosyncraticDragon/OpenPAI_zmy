import numpy as np
import os,sys
import matplotlib.pyplot as plt

def create_city(low=0,up=100):
    x=np.random.uniform(low,up,2)
    return x

def create_cities(num=100):
    cities=np.random.uniform(0,100,(num,2))
    return cities

def save_data(num=100):
    cities=create_cities(num)
    files=os.listdir('./TSP/')
    if 'work' not in files:
        os.mkdir('./TSP/work')
    np.save('./TSP/work/cities.npy',cities)

def load_data(filepath):
    cities=np.load(filepath)
    return cities

def distance_matrix(cities):
    num=len(cities)
    matrix=np.zeros((num,num))
    for i in range(num):
        for j in range(i+1,num):
            matrix[i][j]=(sum(cities[i]-cities[j])**2)**0.5
            matrix[j][i]=matrix[i][j]
    return matrix

def cost(solution,matrix):
    #tmp=np.copy(solution)
    tmp=np.append(solution,solution[0])
    #print("tmp",tmp)
    n=len(solution)
    cost=0
    for i in range(n):
        cost+=matrix[tmp[i]][tmp[i+1]]
    return cost

def random_solution(num=100):
    return np.random.permutation(num)

def init_solutions(num=10,cities=100):
    solutions=[]
    for i in range(num):
        solutions.append(random_solution(cities))
    return solutions

if __name__=="__main__":
    cities=create_cities(100)
    dist=distance_matrix(cities)
    solution=random_solution()
    c=cost(solution,dist)
    print(c)