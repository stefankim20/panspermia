from mpi4py import MPI
comm = MPI.COMM_WORLD
import time
import matplotlib.pyplot as plt
import pyximport; pyximport.install()
import funcs_poisson
import numpy as np

#variables
exp = [-2,-1,0,1,2]
num = 10
trials = 500
t_step = 10 ** -3
years = 5
cores = 2

index = ['a','b','c','d','e','f','g','h','i','j']
final = ['fa','fb','fc','fd','fe','ff','fg','fh','fi','fj']


if comm.rank == 0: 
	start_time = time.time()

for i in exp:
	atau = 5 * 10**i
	for j in exp:
		etau = 5 * 10**j
		for k in exp:
			ptau = 5 * 10**k

			comm.Barrier()
			r = funcs_poisson.sim(etau,atau,ptau,num,trials,t_step,years)
			print(r)
			comm.Barrier()
			for z in range(cores):
				index[z] = open("count"+str(z)+".txt","w+")
			comm.Barrier()
			for z in range(cores):
				if comm.rank == z:
					index[z].write(str(r))
			comm.Barrier()
			for z in range(cores):
				index[z].close()


			for z in range(cores):
				if comm.rank == z:
					index[z] = open("count"+str(z)+".txt","r")
					final[z] = index[z].read().strip('][').split(', ')
						
			if comm.rank == 0:
				for z in range(cores):
					for j,k in enumerate(final[z]):
						final[z][j] = int(k)
				
				p_final = []
				for j,k in enumerate(final):
					for x,y in enumerate(final[j]):
						if j == 0:
							p_final.append(0)
						p_final[x] += (y/(cores * trials * years/t_step))

				sum = 0
				for i in p_final:
					sum += i

				print(sum)

				print(p_final, etau, atau, trials * cores)
				s = open('a' + str(float(atau)) + 'e' + str(float(etau)) + 'p' + str(float(ptau)) + '.txt',"w+")
				s.write(str(p_final))
				s.close()

				x = np.arange(num+1)
				plt.bar(x, p_final, width=-0.4 ,align='edge')
				plt.xticks(x, ['0','1','2','3'])

			comm.Barrier()
			r = funcs_poisson.sim(etau,atau,10**99,num,trials,t_step,years)
			print(r)
			comm.Barrier()
			for z in range(cores):
				index[z] = open("count"+str(z)+".txt","w+")

			comm.Barrier()
			for z in range(cores):
				if comm.rank == z:
					index[z].write(str(r))

			comm.Barrier()
			for z in range(cores):
				index[z].close()


			for z in range(cores):
				if comm.rank == z:
					index[z] = open("count"+str(z)+".txt","r")
					final[z] = index[z].read().strip('][').split(', ')
						
			if comm.rank == 0:
				for z in range(cores):
					for j,k in enumerate(final[z]):
						final[z][j] = int(k)
				
				p_final = []
				for j,k in enumerate(final):
					for x,y in enumerate(final[j]):
						if j == 0:
							p_final.append(0)
						p_final[x] += (y/(cores * trials * years/t_step))

				sum = 0
				for i in p_final:
					sum += i


				print(sum)

				print(p_final, etau, atau, trials * cores)
				s = open('a' + str(float(atau)) + 'e' + str(float(etau)) + 'nopan.txt',"w+")
				s.write(str(p_final))
				s.close()

				x = np.arange(num+1)
				label = []
				for i in range(num+1):
					label.append(str(i))

				plt.bar(x, p_final, width=0.4, color='red', align='edge')
				plt.xticks(x, label)

				plt.savefig('a' + str(atau) + 'e' + str(etau) + 'p' + str(ptau) + '.png')

				plt.clf()
				p_final.clear()

			comm.Barrier()
			#plt.show()

if comm.rank == 0: 
	print("%s seconds" % (time.time() - start_time))
