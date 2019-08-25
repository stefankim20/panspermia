from mpi4py import MPI
comm = MPI.COMM_WORLD
import time
import matplotlib.pyplot as plt
import pyximport; pyximport.install()
import funcs_poisson
import numpy as np

e = [-2,-1,0,1,2]
num = 10
trials = 500
t_step = 10 ** -3
years = 5


if comm.rank == 0: 
	start_time = time.time()
#variables
for i in e:
	atau = 5 * 10**i
	for j in e:
		etau = 5 * 10**j
		for k in e:
			ptau = 5 * 10**k

			comm.Barrier()
			r = funcs_poisson.sim(etau,atau,ptau,num,trials,t_step,years)
			print(r)
			comm.Barrier()
			f = open("count.txt","w+")
			a = open("count2.txt","w+")
			comm.Barrier()
			if comm.rank == 0: 
				f.write(str(r))
			if comm.rank == 1: 
				a.write(str(r))
			comm.Barrier()
			f.close()
			a.close()

			if comm.rank == 0:
				r = open("count.txt","r")
				if r.mode == 'r':
					results = r.read()
				q = open("count2.txt","r")
				if q.mode == 'r':
					results2 = q.read()

				final = results.strip('][').split(', ')
				final2 = results2.strip('][').split(', ')

				for j,k in enumerate(final):
					final[j] = int(k)

				for j,k in enumerate(final2):
					final2[j] = int(k)

				for j,k in enumerate(final):
					final[j] += final2[j]
				print(final)

				p_final = []
				for i in final:
					p_final.append(i/(2 * trials * years/t_step))

				sum = 0
				for i in p_final:
					sum += i

				print(sum)

				print(p_final, etau, atau, trials * 2)
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
			f = open("count.txt","w+")
			a = open("count2.txt","w+")
			comm.Barrier()
			if comm.rank == 0: 
				f.write(str(r))
			if comm.rank == 1: 
				a.write(str(r))
			comm.Barrier()
			f.close()
			a.close()

			if comm.rank == 0:
				r = open("count.txt","r")
				if r.mode == 'r':
					results = r.read()
				q = open("count2.txt","r")
				if q.mode == 'r':
					results2 = q.read()

				final = results.strip('][').split(', ')
				final2 = results2.strip('][').split(', ')

				for j,k in enumerate(final):
					final[j] = int(k)

				for j,k in enumerate(final2):
					final2[j] = int(k)

				for j,k in enumerate(final):
					final[j] += final2[j]
				print(final)

				p_final = []
				for i in final:
					p_final.append(i/(2 * trials * years/t_step))

				sum = 0
				for i in p_final:
					sum += i

				print(sum)

				print(p_final, etau, atau, trials * 2)
				s = open('a' + str(float(atau)) + 'e' + str(float(etau)) + 'nopan.txt',"w+")
				s.write(str(p_final))
				s.close()

				x = np.arange(num+1)

				label = []
				for i in range(num+1):
					label.append(str(i))

				plt.bar(x, p_final, width=0.4, color='red', align='edge')
				plt.xticks(x, label)

				#plt.savefig('a' + str(atau) + 'e' + str(etau) + 'p' + str(ptau) + '.png')

				plt.clf()
				p_final.clear()

			comm.Barrier()
			#plt.show()

if comm.rank == 0: 
	print("%s seconds" % (time.time() - start_time))

