import sys
from random import uniform,choice
from math import *
import matplotlib.pyplot as plt

def readData(filename):
	f=open(filename,'r')
	lines=f.read().splitlines()
	f.close()
	items=[]
	for i in range(len(lines)):
		item1=[]
		item=lines[i].split(',')
		for v in range(len(item)-5):
			t=float(item[v])
			item1.append(t)
		items.append(item1)
	return items

def minimax(items):
	n=len(items[0])
	minimum=[sys.maxint for i in range(n)]
	maximum=[-sys.maxint for i in range(n)]
	for item in items:
		for j in range(n):
			if(minimum[j]>item[j]):
				minimum[j]=item[j]
			if(maximum[j]<item[j]):
				maximum[j]=item[j]
	return minimum,maximum

def Randommean(items,minimum,maximum,k):
	mean=[[0 for i in range(len(items[0]))] for j in range(k)]
	for i in range(k):
		for j in range(len(items[0])):
			mean[i][j]=uniform(minimum[j]+1,maximum[j]-1)
	return mean

def CalDistance(item,value):
	s=0
	for i in range(2,len(item)-1):
		s+=pow(item[i]-value[i],2)
	return sqrt(s)

def classify(mean,item):
	minimum=sys.maxint
	index=-1
	for i in range(len(mean)):
		dis=CalDistance(item,mean[i])
		if(dis<minimum):
			minimum=dis
			index=i
	return index
	
def InitialCluster(items,mean):
	cluster=[[] for i in range(len(mean))]
	for item in items:
		index=classify(mean,item)
		cluster[index].append(item)
	return cluster	
def UpdateCluster(cluster,mean):
	clusters=[[] for i in range(len(mean))]
	for items in cluster:
		for item in items:
			index=classify(mean,item)
			clusters[index].append(item)
	#print "clusters",len(cluster[0]),len(cluster[1])#,len(cluster[2])
	return clusters
	
def updatemean(cluster,mean):
	n=len(cluster[0][1])
	k=len(mean)
	#print "mean",mean
	means=[[0 for i in range(n)] for j in range(k)]	
	for i in range(k):
		items=cluster[i]
		for j in range(n):
			s=0
			for item in items:
				s+=item[j]
			means[i][j]=round(s/float(len(items)),3)
	
	#mean=means
	clusterk=UpdateCluster(cluster,means)
	if(clusterk==cluster):
		return means,-1	
	return means,clusterk	
	
def plotcluster(cluster):
	color=['r','b','g','c','m']
	for x in cluster:
		c=choice(color)
		xa=[]
		xb=[]
		for item in x:	
			xa.append(item[0])
			xb.append(item[2])
		plt.plot(xa,xb,'o',color=c)
		plt.xlabel('Time')
		plt.ylabel('CO2')
		color.remove(c)
	plt.show()		
	
	
def main():
	k=3
	items=readData('/home/vidya/python/work/git/mean_1st_July_NEW_BOX_White.txt')
	minimum,maximum=minimax(items)
	mean=Randommean(items,minimum,maximum,k)
	cluster=InitialCluster(items,mean)
	#print len(cluster)
	for i in range(100):
		mean,clusterk=updatemean(cluster,mean)
		if (clusterk==-1):
			break
		cluster=clusterk
	#print "mean=",mean
	#print "cluster=",cluster
	plotcluster(cluster)
if __name__ =="__main__":
	main()
