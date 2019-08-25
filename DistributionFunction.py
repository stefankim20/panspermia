import numpy as np
import math
import scipy.integrate as integrate
import time

def sim(etau,atau,ptau,num,trials,t_step,years):

	t = t_step
	#generating planets
	class Planet(list):
		def __init__(self,number):
			self.number = number #smallest is nearest to star

	planets = []
	for i in range(num):
		planets.append(Planet(i+1))
	planets.reverse()

	#abiogenesis per planet
	def life(t,t_step,atau):
		
		for j,k in enumerate(planets):
			#life sustained from past abiogenesis
			if planets[j][len(k)-1] == 1:
				planets[j].append(1)

			#life sustained from past panspermia
			elif planets[j][len(k)-1] == 2:
				planets[j].append(2)

			#new abiogenesis
			elif planets[j][len(k)-1] == 0:
				if np.random.poisson(lam=t_step/atau) >= 1:
					planets[j].append(1)
				else:
					planets[j].append(0)		
			#print ('a',j,planets[j][len(k)-1],abio[len(abio)-1],pans[len(pans)-1])

	#panspermia to next planet	
	def pan(t,t_step,ptau):
		
		for j,k in enumerate(planets):
			if k[len(k)-2] >= 1:
				i = 1
				while i < k.number:
					if np.random.poisson(lam=t_step/ptau) >= 1:
						if planets[j+i][len(k)-1] == 0:
							planets[j+i][len(k)-1] = 2
						#planets[j+i][len(k)-1] = 1
					i += 1
			#print ('p',j,planets[j][len(k)-1],abio[len(abio)-1],pans[len(pans)-1])	


	#extinction per planet
	def ext(t,t_step,etau):

		for j,k in enumerate(planets):
			if np.random.poisson(lam=t_step/etau) >= 1:
				if planets[j][len(k)-1] >= 1:
					planets[j][len(k)-1] = 0
			#print('e',j,planets[j][len(k)-1],abio[len(abio)-1],pans[len(pans)-1])



	#trials
	counter = []
	counter_t = []
	for i in range(num+1):
		counter_t.append(0)

	est = time.time()
	for r in range(trials):
		begin = time.time()
		t = t_step
		#at t=0, all planets have no life... also get index out of range error
		for j,k in enumerate(planets):
			k.clear()
			k.append(0)

		counter.clear()
		counter.append(0)

		while t < years:

			life(t,t_step,atau)
			pan(t,t_step,ptau)
			ext(t,t_step,etau)

			counter.append(0)
			t += t_step

		#life on each planet to number of life at each timestep
		for j,k in enumerate(planets):
			for x,y in enumerate(k):
				if y == 1:
					counter[x] += 1
				if y == 2:
					counter[x] += 1

		#life at each timestep to count of number of planets w life
		for i in counter:
			counter_t[i] += 1

		if r == 0:
			print("estimated %s seconds" % ((time.time() - begin) * trials))

		print (100 * float(r/trials), "%", counter_t)

	return counter_t
